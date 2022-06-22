// IPK Projekt 2 - ZETA
// ipk-sniffer.cpp
// version 1.0
// Jakub Duda, xdudaj02


/* This project is Copyright 2002 Tim Carstens.
 * All rights reserved. Redistribution and use, with or without modification,
 * are permitted provided that the following conditions are met:
 *  1. Redistribution must retain the above copyright notice and this list of conditions.
 *  2. The name of Tim Carstens may not be used to endorse or promote products derived
 *     from this document without specific prior written permission.
 */


#include <iostream>
#include <cstdlib>
#include <unistd.h>
#include <getopt.h>
#include <pcap/pcap.h>
#include <netinet/in.h>
#include <netinet/ether.h>
#include <arpa/inet.h>
#include <sstream>
#include <iomanip>
#include <csignal>

using namespace std;

/* GLOBAL VARIABLES */
pcap_t *handle = nullptr;  // handle for a device (interface) to sniff on

/* CONSTANTS */
const int ARG_ERROR = 1;  // argument error exit code
const int SNIFFER_ERROR = 2;  // sniffer error exit code
const int LINE_LENGTH = 16;  // line length when outputting packet content

// fixed header sizes
#define SIZE_ETHERNET_HEADER 14  // ethernet header size
#define SIZE_IPV6_HEADER 40  // ipv6 header size

/* STRUCTURES */
// Ethernet header structure
// inspired by: https://www.tcpdump.org/pcap.html
struct ethernet_header {
    u_char  ether_dhost[ETHER_ADDR_LEN];  // destination host address
    u_char  ether_shost[ETHER_ADDR_LEN];  // source host address
    u_short ether_type;  // type of next header (arp/ip/ipv6)
};

// IPv4 header structure
struct ipv4_header {
    u_char ipv4_vhl;  // version (first 4 bits), header length (last 4 bits)
    u_char ipv4_tos;  // type of service
    u_short ipv4_len;  // total length
    u_short ipv4_id;  // identification
    u_short ipv4_off;  // fragment offset field
    u_char ipv4_ttl;  // time to live
    u_char ipv4_p;  // protocol type
    u_short ipv4_sum;  // checksum
    struct in_addr ipv4_src, ipv4_dst;  // source and destination ip addresses
};
#define IP_HL(ip) (((ip)->ipv4_vhl) & 0x0f)  // returns header length
#define IP_V(ip) (((ip)->ip_vhl) >> 4)  // returns version

// IPv6 header structure
struct ipv6_header {
    u_int ip6_vtcfl;  // version (first 4 bits), traffic class (next 8 bits), flow label (last 20 bits)
    u_short ipv6_pll;  // payload length
    u_char ipv6_nhd;  // next header type
    u_char ipv6_hop;  // hop limit
    in6_addr ipv6_src;  // source ip address
    in6_addr ipv6_dst;  // destination ip address
};

// ARP header structure
struct arp_header {
    u_short arp_hwtype;  // hardware type
    u_short arp_ptype;  // protocol type
    u_char arp_hwlen;  // hardware address length
    u_char arp_plen;  // protocol address length
    u_short arp_oper;  // operation
    u_char arp_src_mac[ETHER_ADDR_LEN];  // source hardware address (mac)
    struct in_addr arp_src;  // source protocol address (ip)
    u_char arp_dst_mac[ETHER_ADDR_LEN];  // destination hardware address (mac)
    struct in_addr arp_dst;  // destination protocol address (ip)
} __attribute__((packed)); // necessary because of hw address length

// TCP header structure
struct tcp_header {
    u_short th_sport;  // source port
    u_short th_dport;  // destination port
    u_int th_seq_num;  // sequence number
    u_int th_ack_num;  // acknowledgement number
    u_char th_offx2;  // header length (first 4 bits), reserved bites
#define TH_OFF(th) (((th)->th_offx2 & 0xf0) >> 4)  // returns header length / data offset
    u_char th_flags;  //flags
    u_short th_win;  // window
    u_short th_sum;  // checksum
    u_short th_urp;  // urgent pointer
};

// UCP header structure
struct udp_header {
    u_short uh_sport;  // source port
    u_short uh_dport;  // destination port
    u_short uh_len;  // length
    u_short uh_sum;  // checksum
};

// ICMP header structure
struct icmp_header {
    u_char icmp_type;  // type
    u_char icmp_code;  // code
    u_short icmp_sum;  // checksum
    u_int icmp_unused; // unused bits
};


/* FUNCTIONS */
// function takes time value passed in timeval structure and returns it in string formatted according to RFC3339 standard
string format_time(timeval time) {
    char date[50];  // buffer
    strftime(date, 50, "%FT%T", localtime(&time.tv_sec));  // calculate date and time from seconds since epoch
    stringstream ss;
    // concatenate date and time, milliseconds (3 digits) and local timezone
    // inspired by: https://stackoverflow.com/questions/54325137/c-rfc3339-timestamp-with-milliseconds-using-stdchrono
    //      question: sebastian, https://stackoverflow.com/users/1523730/sebastian
    //      answer: Howard Hinnant, https://stackoverflow.com/users/576911/howard-hinnant
    ss << date << "." << setfill('0') << setw(3) << (time.tv_usec / 1000) << "+02:00";
    return ss.str();
}

// function prints formatted packet content (headers and data)
// format: offset  hexadecimal data                                  ascii data
//         0x0000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ........ ........
void print_packet_content(bpf_u_int32 length, const u_char *packet) {
    stringstream ascii;
    // loop over the whole packet
    for (int i = 0; i < length; i++) {
        if ((i % LINE_LENGTH) == 0)
            printf("\n0x%04x: ", i);  // print line start (data offset)
        printf(" %02hhx", packet[i]);  // print one byte of data in hexadecimal
        if (isprint(packet[i]))  // add byte of data to ascii string
            ascii << packet[i];  // if printable
        else
            ascii << ".";  // replace unprintable characters with '.'
        if ((i % LINE_LENGTH) == 7) {  // add extra space after 8 bytes for visual aid
            printf(" ");
            ascii << " ";
        }
        if ((i % LINE_LENGTH) == 15 || (i + 1) == length) {  // on end of line or end of data
            if ((i + 1) == length){  // if end of data
                for (int j = 0; j < (16 - (i % 16 + 1)); j++)  // print remaining indent in front of data in ascii
                    printf("   ");
                if ((i % LINE_LENGTH) < 7 && (i % 16) > 0)  // add extra space if line is shorter than 8
                    printf(" ");
            }
            printf("  %s", ascii.str().c_str());  // print data in ascii
            // clear stringstream used for printing data in ascii
            ascii.str("");
            ascii.clear();
        }
    }
    printf("\n\n\n");  // print indent after package
}

// function for handling icmp packets
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data,
//            size_ip - size of ip header, src_ip - source ip address, dst_ip - destination ip address
void handle_icmp(u_char *args, const struct pcap_pkthdr *header, const u_char *packet, int size_ip, in_addr src_ip, in_addr dst_ip) {
    //printf("ICMP\n");

    // print header of packet output
    printf("%s %s > ", format_time(header->ts).c_str(), inet_ntoa(src_ip));  // time, source ip address
    printf("%s, length %i bytes\n", inet_ntoa(dst_ip), header->caplen);  // dest ip address, length in bytes

    // print packet content
    print_packet_content(header->caplen, packet);
}

// function for handling udp packets
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data,
//            size_ip - size of ip header, src_ip - source ip address, dst_ip - destination ip address
void handle_udp(u_char *args, const struct pcap_pkthdr *header, const u_char *packet, int size_ip, in_addr src_ip, in_addr dst_ip) {
    //printf("UDP\n");
    const struct udp_header *udp;  // udp header structure instance

    // cast packet with calculated offset to udp header structure
    udp = (struct udp_header*)(packet + SIZE_ETHERNET_HEADER + size_ip);

    // print header of packet output
    printf("%s %s : %hu > ", format_time(header->ts).c_str(), inet_ntoa(src_ip), ntohs(udp->uh_sport));
    printf("%s : %hu, length %i bytes\n", inet_ntoa(dst_ip), ntohs(udp->uh_dport), header->caplen);

    // print packet content
    print_packet_content(header->caplen, packet);
}

// function for handling tcp packets
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data,
//            size_ip - size of ip header, src_ip - source ip address, dst_ip - destination ip address
void handle_tcp(u_char *args, const struct pcap_pkthdr *header, const u_char *packet, int size_ip, in_addr src_ip, in_addr dst_ip) {
    //printf("TCP\n");
    const struct tcp_header *tcp;  // tcp header structure instance
    int size_tcp;  // size of tcp header

    // cast packet with calculated offset to tcp header structure
    tcp = (struct tcp_header*)(packet + SIZE_ETHERNET_HEADER + size_ip);

    size_tcp = TH_OFF(tcp)*4;  // calculate tcp header size
    if (size_tcp < 20) {  // check tcp header size
        fprintf(stderr, "ipk-sniffer - SNIFFER ERROR: packet with invalid tcp header\n");
        return;
    }

    // print header of packet output
    printf("%s %s : %hu > ", format_time(header->ts).c_str(), inet_ntoa(src_ip), ntohs(tcp->th_sport));
    printf("%s : %hu, length %i bytes\n", inet_ntoa(dst_ip), ntohs(tcp->th_dport), header->caplen);

    // print packet content
    print_packet_content(header->caplen, packet);
}

// function for handling icmpv6 packets
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data,
//            src_ip - source ipv6 address, dst_ipv6 - destination ip address
void handle_icmpv6(u_char *args, const struct pcap_pkthdr *header, const u_char *packet, in6_addr src_ip, in6_addr dst_ip) {
    //printf("ICMPv6\n");
    char ipv6_addr[INET6_ADDRSTRLEN];  // buffer

    // print header of packet output
    inet_ntop(AF_INET6, &src_ip, ipv6_addr, INET6_ADDRSTRLEN);  // get formatted string of ipv6 src address
    printf("%s %s > ", format_time(header->ts).c_str(), ipv6_addr);
    inet_ntop(AF_INET6, &dst_ip, ipv6_addr, INET6_ADDRSTRLEN);  // get formatted string of ipv6 dst address
    printf("%s, length %i bytes\n", ipv6_addr, header->caplen);

    // print packet content
    print_packet_content(header->caplen, packet);
}

// function for handling udp packets preceded by ipv6 header
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data,
//            src_ip - source ipv6 address, dst_ipv6 - destination ip address
void handle_udpv6(u_char *args, const struct pcap_pkthdr *header, const u_char *packet, in6_addr src_ip, in6_addr dst_ip) {
    //printf("UDPv6\n");
    char ipv6_addr[INET6_ADDRSTRLEN];  // buffer
    const struct udp_header *udp;  // udp header structure instance

    // cast packet with calculated offset to udp header structure
    udp = (struct udp_header*)(packet + SIZE_ETHERNET_HEADER + SIZE_IPV6_HEADER);

    // print header of packet output
    inet_ntop(AF_INET6, &src_ip, ipv6_addr, INET6_ADDRSTRLEN);  // get formatted string of ipv6 src address
    printf("%s %s : %hu > ", format_time(header->ts).c_str(), ipv6_addr, ntohs(udp->uh_sport));
    inet_ntop(AF_INET6, &dst_ip, ipv6_addr, INET6_ADDRSTRLEN);  // get formatted string of ipv6 dst address
    printf("%s : %hu, length %i bytes\n", ipv6_addr, ntohs(udp->uh_dport), header->caplen);

    // print packet content
    print_packet_content(header->caplen, packet);
}

// function for handling tcp packets preceded by ipv6 header
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data,
//            src_ip - source ipv6 address, dst_ipv6 - destination ip address
void handle_tcpv6(u_char *args, const struct pcap_pkthdr *header, const u_char *packet, in6_addr src_ip, in6_addr dst_ip) {
    //printf("TCPv6\n");
    char ipv6_addr[INET6_ADDRSTRLEN];  // buffer
    const struct tcp_header *tcp;  // tcp header structure instance
    int size_tcp;  // size of tcp header

    // cast packet with calculated offset to tcp header structure
    tcp = (struct tcp_header*)(packet + SIZE_ETHERNET_HEADER + SIZE_IPV6_HEADER);

    size_tcp = TH_OFF(tcp)*4;  // calculate tcp header size
    if (size_tcp < 20) {  // check tcp header size
        fprintf(stderr, "ipk-sniffer - SNIFFER ERROR: packet with invalid tcp header\n");
        return;
    }

    // print header of packet output
    inet_ntop(AF_INET6, &src_ip, ipv6_addr, INET6_ADDRSTRLEN);  // get formatted string of ipv6 src address
    printf("%s %s : %hu > ", format_time(header->ts).c_str(), ipv6_addr, ntohs(tcp->th_sport));
    inet_ntop(AF_INET6, &dst_ip, ipv6_addr, INET6_ADDRSTRLEN);  // get formatted string of ipv6 dst address
    printf("%s : %hu, length %i bytes\n", ipv6_addr, ntohs(tcp->th_dport), header->caplen);

    // print packet content
    print_packet_content(header->caplen, packet);
}

// function for handling arp packets
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data
void handle_arp(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
    //printf("ARP\n");
    const struct arp_header *arp;  // arp header structure instance

    // cast packet with calculated offset to arp header structure
    arp = (struct arp_header*)(packet + SIZE_ETHERNET_HEADER);

    // print header of packet output
    printf("%s %s > ", format_time(header->ts).c_str(), ether_ntoa((struct ether_addr*)arp->arp_src_mac));
    printf("%s, length %i bytes\n", ether_ntoa((struct ether_addr*)arp->arp_dst_mac), header->caplen);

    // print packet content
    print_packet_content(header->caplen, packet);
}

// function for handling ipv4 packets
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data
void handle_ipv4(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
    const struct ipv4_header *ip;  // ipv4 header structure instance
    int size_ip;  // size of ipv4 header

    // cast packet with calculated offset to ipv4 header structure
    ip = (struct ipv4_header*)(packet + SIZE_ETHERNET_HEADER);
    size_ip = IP_HL(ip)*4;  // calculate ipv4 header size
    if (size_ip < 20) {  // check ipv4 header size
        fprintf(stderr, "ipk-sniffer - SNIFFER ERROR: packet with invalid ip header\n");
        return;
    }

    // determine protocol (next header) and call respective function
    switch(ip->ipv4_p) {
        case IPPROTO_TCP:  // tcp
            handle_tcp(args, header, packet, size_ip, ip->ipv4_src, ip->ipv4_dst);
            break;
        case IPPROTO_UDP:  // udp
            handle_udp(args, header, packet, size_ip, ip->ipv4_src, ip->ipv4_dst);
            break;
        case IPPROTO_ICMP:  // icmp
            handle_icmp(args, header, packet, size_ip, ip->ipv4_src, ip->ipv4_dst);
            break;
        default:
            break;
    }
}

// function for handling ipv6 packets
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data
void handle_ipv6(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
    const struct ipv6_header *ip;  // ipv6 header structure instance

    // cast packet with calculated offset to ipv6 header structure
    ip = (struct ipv6_header*)(packet + SIZE_ETHERNET_HEADER);

    // determine protocol (next header) and call respective function
    switch(ip->ipv6_nhd) {
        case IPPROTO_TCP:  // tcp
            handle_tcpv6(args, header, packet, ip->ipv6_src, ip->ipv6_dst);
            break;
        case IPPROTO_UDP:  // udp
            handle_udpv6(args, header, packet, ip->ipv6_src, ip->ipv6_dst);
            break;
        case IPPROTO_ICMP:  // icmp
            handle_icmpv6(args, header, packet, ip->ipv6_src, ip->ipv6_dst);
            break;
        default:
            break;
    }
}

// function for handling Ethernet packets
// arguments: args - last argument of pcap_loop, header - packet header, packet - packet content/data
void handle_ether(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
    const struct ethernet_header *ethernet;  // Ethernet header structure instance

    // cast packet to Ethernet header structure
    ethernet = (struct ethernet_header*)(packet);

    // determine protocol (next header) and call respective function
    switch (ntohs(ethernet->ether_type)) {
        case ETHERTYPE_ARP:  // arp
            handle_arp(args, header, packet);
            break;
        case ETHERTYPE_IP:  // ipv4
            handle_ipv4(args, header, packet);
            break;
        case ETHERTYPE_IPV6:  // ipv6
            handle_ipv6(args, header, packet);
            break;
        default:
            break;
    }
}

// function prints all available devices returned by pcap_findalldevs() and exits
void print_all_devs() {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_if_t *alldevs;
    pcap_if_t *d;
    // get all available devices
    if (pcap_findalldevs(&alldevs, errbuf) == -1) {  // on error
        fprintf(stderr, "ipk-sniffer - SNIFFER ERROR: no devices found\n%s\n", errbuf);
        exit(SNIFFER_ERROR);
    }

    // print all available devices
    for(d = alldevs; d != nullptr; d= d->next)
        printf("%s\n", d->name);
    exit(EXIT_SUCCESS);
}


// function for handling the interrupt signal (ctrl+c)
void signal_callback_handler(int signum) {
    if (handle != nullptr)
        pcap_close(handle);  // close device handle if not null
    exit(signum);
}


/* MAIN FUNCTION */
int main(int argc, char** argv) {
    // definitions and declarations of used variables
    int c;
    char* interface;  // interface to sniff on
    int num_packets = 1;  // number of packets to sniff
    int port_specified = 0;  // specified port for sniffing
    int i_used = 0;  // usage of mandatory i argument
    int tcp = 0;  // usage of tcp flag
    int udp = 0;  // usage of udp flag
    int arp = 0;  // usage of arp flag
    int icmp = 0;  // usage of icmp flag
    string filter_exp;  // string for expression used to create a filter fro sniffing
        struct bpf_program fp{};  // structure for filter
    char errbuf[PCAP_ERRBUF_SIZE];  // buffer for error messages

    // signal handler for program interruption
    // inspired by: https://www.tutorialspoint.com/how-do-i-catch-a-ctrlplusc-event-in-cplusplus
    signal(SIGINT, signal_callback_handler);

    // parsing of command line options
    while (true) {
        int option_index = 0;
        static struct option long_options[] = {  // structure for long command line options
                {"interface", required_argument, nullptr, 'i'},
                {"tcp", no_argument, nullptr, 't'},
                {"udp", no_argument, nullptr, 'u'},
                {"arp", no_argument, nullptr, 'a'},
                {"icmp", no_argument, nullptr, 'c'}
        };

        c = getopt_long(argc, argv, ":i:p:n:tu", long_options, &option_index);  // get next cl option
        if (c == -1)  // no more cl options
            break;

        switch (c) {
            // -i|--interface
            case 'i':
                interface = optarg;
                i_used++;
                break;

            // -p (port)
            case 'p':
                try {
                    port_specified = stoi(optarg);
                } catch (exception&) {
                        fprintf(stderr, "ipk_sniffer - ARGUMENT ERROR: invalid argument value\n");
                        exit(ARG_ERROR);
                }
                break;

            // -n (number of packets)
            case 'n':
                try {
                    num_packets = stoi(optarg);
                } catch (exception&) {
                    fprintf(stderr, "ipk_sniffer - ARGUMENT ERROR: invalid argument value\n");
                    exit(ARG_ERROR);
                }
                break;

            // -t|--tcp
            case 't':
                tcp++;
                break;

            // -u|--udp
            case 'u':
                udp++;
                break;

            // --arp
            case 'a':
                arp++;
                break;

            // --icmp
            case 'c':
                icmp++;
                break;

            // cl option missing a mandatory argument
            case ':':
                if (optopt == 'i') {  // interface argument missing
                    print_all_devs();
                }  // else error
                fprintf(stderr, "ipk_sniffer - ARGUMENT ERROR: argument missing a mandatory parameter\n");
                exit(ARG_ERROR);

            // unsupported cl option -> error
            case '?':
                fprintf(stderr, "ipk_sniffer - ARGUMENT ERROR: invalid argument used\n");
                exit(ARG_ERROR);

            default:
                break;
        }
    }

    // interface option not used
    if (!i_used) {
        print_all_devs();
    }

    // generating filter string
    int protocol_specified = (tcp || udp || arp || icmp);  // protocol options used
    if (!protocol_specified) {  // no protocols specified
        if (!port_specified)  // port not specified
            filter_exp = "tcp or udp or arp or icmp";  // default
        else  // port specified
            filter_exp = "tcp port " + to_string(port_specified) + " or udp port " + to_string(port_specified) + " or arp or icmp";
    } else {
        if (arp)
            filter_exp.append("arp or ");
        if (icmp)
            filter_exp.append("icmp or ");
        if (!port_specified) {
            if (tcp)
                filter_exp.append("tcp or ");
            if (udp)
                filter_exp.append("udp or ");
        } else {
            if (tcp)
                filter_exp.append("tcp port " + to_string(port_specified) + " or ");
            if (udp)
                filter_exp.append("udp port " + to_string(port_specified) + " or ");
        }
        filter_exp = filter_exp.substr(0, filter_exp.size() - 4); // remove " or " from the end of filter string
    }
    //printf("%s", filter_exp.c_str());

    // initialize device handle
    handle = pcap_create(interface, errbuf);
    if (handle == nullptr) {  // error
        fprintf(stderr, "ipk-sniffer - SNIFFER ERROR: opening of device failed\n%s\n", errbuf);
        exit(SNIFFER_ERROR);
    }
    pcap_set_promisc(handle, 1);  // set promiscuous mode
    pcap_set_timeout(handle, 1);

    int err;
    // activate handle
    if ((err = pcap_activate(handle)) < 0) {
        // error
        pcap_perror(handle, "ipk-sniffer - SNIFFER ERROR: device activation failed\n");
        pcap_close(handle);
        exit(SNIFFER_ERROR);
    }
    else if (err > 0) {
        // warning
        pcap_perror(handle, "ipk-sniffer - SNIFFER WARNING:\n");
    }

    // check if interface is Ethernet, else error
    if (pcap_datalink(handle) != DLT_EN10MB) {
        fprintf(stderr, "ipk-sniffer - SNIFFER ERROR: usage of unsupported interface\n");
        exit(SNIFFER_ERROR);
    }

    // compile filter
    if (pcap_compile(handle, &fp, filter_exp.c_str(), 0, PCAP_NETMASK_UNKNOWN) == -1) {
        // error
        pcap_perror(handle, "ipk-sniffer - SNIFFER ERROR: filter parsing failed\n");
        exit(SNIFFER_ERROR);
    }

    // apply the compiled filter
    if (pcap_setfilter(handle, &fp) == -1) {
        // error
        pcap_perror(handle, "ipk-sniffer - SNIFFER ERROR: filter installation failed\n");
        exit(SNIFFER_ERROR);
    }
    pcap_freecode(&fp);  // free the filter structure

    // sniff num_packets of packets on handle, uses callback function handle_ether()
    pcap_loop(handle, num_packets, handle_ether, nullptr);

    pcap_close(handle);  // close handle

    return EXIT_SUCCESS;
}

// end of file