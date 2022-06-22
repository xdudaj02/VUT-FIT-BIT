// ISA Projekt 1 - Klient POP3
// popcl.cpp
// version 1.0
// 13. 11. 2021
// Jakub Duda, xdudaj02

/* INCLUDES */
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstring>
#include <sys/stat.h>

# include  "openssl/bio.h"
# include  "openssl/ssl.h"
# include  "openssl/err.h"

using namespace std;

/* CONSTANTS */
const int POPCL_OK = 0; // ok exit code
const int ARG_ERR = 1;  // argument error exit code
const int OPENSSL_ERR = 2;  // openssl error exit code
const int POPCL_ERR = 3;  // popcl program error exit code

const int PORT_INVALID = -1; // initial value, port not set
const int PORT_POP3 = 110; // default port used by pop3
const int PORT_POP3S = 995; // default port used by pop3s

const char username_string[] = "username = "; //mandatory string in authentication file that is followed by a username
const char password_string[] = "password = "; //mandatory string in authentication file that is followed by a password

const int BUF_SIZE = 1024; // size of buffer used for message exchange with server
const int INT_INVALID = -1; // invalid int value error

/* STRUCTURES */
// internal structure for used data
struct data {
    string server; // address of server
    string username; // username that is used
    string password; // password for used username
    string out_dir; // directory for saving email files
    bool msg_del = false; // if true all messages will be deleted from server
    bool msg_new = false; // if true only new messages are downloaded
    int port = PORT_INVALID; // port number to use
    bool pop3s = false; // if true secure pop3s connection is used
    bool stls = false; // if true unsecure pop3 connection is right away upgraded by the STLS command
    string cert_dir; // directory to search for certificates
    string cert_file; // file with certificates
    SSL_CTX *ctx = nullptr; // certificate object for secure connection
};

/* CLASSES */
// argument exception, thrown when invalid command line options usage is detected
class arg_exception: public runtime_error {
    using runtime_error::runtime_error;
};

/* FUNCTIONS */
// function for retrieving authentication data from provided authentication file, throws arg_exception
void get_auth_data(data* popcl_data, const string& auth_file) {
    ifstream infile;
    infile.open(auth_file);
    if (!infile.is_open())
        throw arg_exception("popcl - ARGUMENT ERROR: invalid value for argument '-a' (cannot access file with this name)\n");
    string line;
    // get username
    getline(infile, line);
    if (line.length() < 12 or line.substr(0, 11) != username_string)
        throw arg_exception("popcl - ARGUMENT ERROR: invalid authentication file format\n");
    popcl_data->username = line.substr(11);
    // get password
    getline(infile, line);
    if (line.length() < 12 or line.substr(0, 11) != password_string)
        throw arg_exception("popcl - ARGUMENT ERROR: invalid authentication file format\n");
    popcl_data->password = line.substr(11);
    infile.close();
}

// function for parsing command line options, throws arg_exception
void parse_args(int argc, char** argv, data* popcl_data) {
    string auth_file;

    if (argc < 2 or argc > 15) {
        throw arg_exception("popcl - ARGUMENT ERROR: invalid number of arguments used\n");
    }

    // <server> :mandatory, must be the first argument, string indicating the name or the ip address of the server
    popcl_data->server = argv[1];

    for (int i = 2; i < argc; i++) {
        if (argv[i][0] == '-' && argv[i][2] == '\0') {
            switch (argv[i][1]) {
                // -a <auth_file> :mandatory, string describing path to file containing authorization details
                case 'a':
                    if (i == (argc - 1)) {
                        throw arg_exception("popcl - ARGUMENT ERROR: argument '-a' missing value\n");
                    }
                    auth_file = argv[++i];
                    break;

                // -o <out_dir> :mandatory, string containing path to output directory where mails will be saved
                case 'o':
                    if (i == (argc - 1)) {
                        throw arg_exception("popcl - ARGUMENT ERROR: argument '-o' missing value\n");
                    }
                    popcl_data->out_dir = argv[++i];
                    break;

                // -p <port_num> :optional, integer indicating port number
                case 'p':
                    if (i == (argc - 1)) {
                        throw arg_exception("popcl - ARGUMENT ERROR: argument '-p' missing value\n");
                    }
                    try {
                        popcl_data->port = stoi(argv[++i]);
                    }
                    catch (exception&) {
                        throw arg_exception("popcl - ARGUMENT ERROR: invalid value for argument '-p' (must be integer)\n");
                    }
                    if (popcl_data->port < 0) {
                        throw arg_exception("popcl - ARGUMENT ERROR: invalid value for argument '-p' (must be positive integer)\n");
                    }
                    break;

                // -d :optional, no value, when used messages will be deleted from server
                case 'd':
                    popcl_data->msg_del = true;
                    break;

                // -n :optional, no value, when used program will only consider new messages
                case 'n':
                    popcl_data->msg_new = true;
                    break;

                // -T :optional, no value, when used secure pop3s protocol will be used in place of pop3,
                //     must not be used in combination with '-S'
                case 'T':
                    if (popcl_data->stls) {
                        throw arg_exception("popcl - ARGUMENT ERROR: invalid argument combination (only one of '-T' and '-S' can be used)\n");
                    }
                    popcl_data->pop3s = true;
                    break;

                // -S :optional, no value, when used security layer will be activated using the STLS command,
                //     must not be used in combination with '-T'
                case 'S':
                    if (popcl_data->pop3s) {
                        throw arg_exception("popcl - ARGUMENT ERROR: invalid argument combination (only one of '-T' and '-S' can be used)\n");
                    }
                    popcl_data->stls = true;
                    break;

                // -c <cert_file> :optional, string specifying path to certificate file, must be used in combination
                //                 with '-S' or '-T'
                case 'c':
                    if (i == (argc - 1)) {
                        throw arg_exception("popcl - ARGUMENT ERROR: argument '-c' missing value\n");
                    }
                    popcl_data->cert_file = argv[++i];
                    break;

                // -C <cert_dir> :optional, string specifying path to directory that is to be searched for certificate
                //                files, must be used in combination with '-S' or '-T'
                case 'C':
                    if (i == (argc - 1)) {
                        throw arg_exception("popcl - ARGUMENT ERROR: argument '-C' missing value\n");
                    }
                    popcl_data->cert_dir = argv[++i];
                    break;
                default:
                    throw arg_exception("popcl - ARGUMENT ERROR: invalid argument used\n");
            }
        } else {
            throw arg_exception("popcl - ARGUMENT ERROR: invalid argument used\n");
        }
    }

    // check for usage of mandatory arguments
    if (auth_file.empty()) {
        throw arg_exception("popcl - ARGUMENT ERROR: mandatory argument '-a' missing\n");
    }
    if (popcl_data->out_dir.empty()) {
        throw arg_exception("popcl - ARGUMENT ERROR: mandatory argument '-o' missing\n");
    }

    // try to retrieve authentication details from provided authentication file
    get_auth_data(popcl_data, auth_file);

    // check existence / accessibility of output directory
    //      (so user does not have to wait for the whole pop3 communication to execute to discover this)
    // inspred by:
    //      name: Portable way to check if directory exists [Windows/Linux, C]
    //      date: 11.11.2021
    //      source: https://stackoverflow.com/questions/18100097/portable-way-to-check-if-directory-exists-windows-linux-c
    //      question: https://stackoverflow.com/users/2656473/ivy
    //      answer: https://stackoverflow.com/users/2470782/ingo-leonhardt
    struct stat info{};
    if (!((not stat((popcl_data->out_dir).c_str(), &info)) and (info.st_mode & S_IFDIR)))
        throw arg_exception("popcl - ARGUMENT ERROR: invalid value for argument '-o' (cannot access directory with this name)\n");

    // check existence of special directory .config, error is non-critical but disables the functionality of '-n'
    if (!((not stat(".config", &info)) and (info.st_mode & S_IFDIR)))
        fprintf(stderr, "popcl - ARGUMENT ERROR: cannot access directory .config, functionality of '-n' is disabled\n");

    // check for usage of illegal argument combinations
    if((!(popcl_data->cert_file.empty()) or !(popcl_data->cert_dir.empty())) and !(popcl_data->pop3s or popcl_data->stls)) {
        throw arg_exception("popcl - ARGUMENT ERROR: invalid argument combination (arguments '-c' and '-C' can only be used in combination with arguments '-T' or '-S')\n");
    }

    // set default port number if not provided as argument
    if (popcl_data->port == PORT_INVALID) {
        popcl_data->port = popcl_data->pop3s ? PORT_POP3S : PORT_POP3;
    }
}

// free used memory, exit with error code and print error string to stderr
void error_exit(data *popcl_data, BIO *bio, int exit_code, const string& error_string){
    // free resources
    if (bio) {
        BIO_free_all(bio);
    }
    if (popcl_data->ctx) {
        SSL_CTX_free(popcl_data->ctx);
    }
    delete popcl_data;

    fprintf(stderr, "%s", error_string.c_str()); // print error
    exit(exit_code); // exit with provided error code
}

// reads response from server, on error function ends program with exit code POPCL_ERR
bool pop3_read(data *popcl_data, BIO *bio, char* buf, bool check_response) {
    // clear buffer
    memset(buf, '\0', BUF_SIZE);

    // try to read, handle error
    if (BIO_read(bio, buf, BUF_SIZE - 1) <= 0) {
        error_exit(popcl_data, bio, OPENSSL_ERR, "popcl - OPENSSL ERROR\n");
    }

    // not expecting response of type '+OK' or '-ERR'
    if (!check_response) {
        return true;
    }

    string response = buf;
    // if '+OK' -> return true else false
    return (!((response.length() < 3) or (response.substr(0, 3) != "+OK")));
}

// writes provided message to server, on error function ends program with exit code POPCL_ERR
void pop3_write(data *popcl_data, BIO *bio, const string& msg) {
    if(BIO_write(bio, (msg + "\r\n").c_str(), msg.length() + 2) <= 0) {
        error_exit(popcl_data, bio, OPENSSL_ERR, "popcl - OPENSSL ERROR\n");
    }
}

// writes provided message to server, reads the response and returns outcome
bool pop3_write_and_read(data *popcl_data, BIO *bio,  char* buf, const string& msg) {
    pop3_write(popcl_data, bio, msg);
    return pop3_read(popcl_data, bio, buf, true);
}

// get and return number of emails from server response (to STAT command)
int pop3_get_number(const string& response) {
    // expected response: "+OK number length"
    int number;
    try {
        number = stoi(response.substr(4, response.substr(4).find(' ')));
    }
    catch (exception&) {
        return INT_INVALID;
    }
    return number;
}

// get and return email length from server response (to LIST <num> command)
int pop3_get_length(const string& response, int number) {
    // expected response: "+OK number length"
    string tmp = "+OK " + to_string(number) + " ";
    if ((response.length() < tmp.length()) or (response.substr(0, tmp.length()) != tmp)) {
        return INT_INVALID;
    }

    int length;
    try {
        length = stoi(response.substr(tmp.length()));
    }
    catch (exception&) {
        return INT_INVALID;
    }

    if (response != (tmp + to_string(length) + "\r\n")) {
        return INT_INVALID;
    }

    return length;
}

// try to get message id from the content of a mail, returns string containing the message id or empty string if not found
string get_msg_id(const string& content) {
    // valid message id names
    string msg_id_start_string_a = "\r\nMessage-ID: <";
    string msg_id_start_string_b = "\r\nMessage-Id: <";

    // get start of msg id
    size_t msg_id_start = content.find(msg_id_start_string_a); // try version a
    if (msg_id_start == string::npos) {
        msg_id_start = content.find(msg_id_start_string_b); // try version b
        if (msg_id_start == string::npos) {
            return ""; // mail does not contain its message id
        }
    }
    msg_id_start += msg_id_start_string_a.length();

    // get end of msg id
    size_t msg_id_end = content.substr(msg_id_start).find(">\r\n");
    if (msg_id_end == string::npos) {
        return "";
    }

    return content.substr(msg_id_start, msg_id_end);
}

// save message id in the special message id file
void save_msg_id(const string& msg_id, const string& recipient_addr) {
    if (msg_id.empty()) {
        return;
    }

    ofstream msg_id_file;
    msg_id_file.open(".config/" + recipient_addr, ios_base::app);
    msg_id_file << "\n" << msg_id << "\n";
    msg_id_file.close();
}

// search message id in the special message id file, returns true if message is new
bool check_msg_id(const string& msg_id, const string& recipient_addr) {
    if (msg_id.empty()) {
        return true;
    }

    ifstream msg_id_file;
    msg_id_file.open(".config/" + recipient_addr);
    stringstream buffer;
    buffer << msg_id_file.rdbuf();

    return (buffer.str().find("\n" + msg_id + "\n") == string::npos);
}

// get recipient address as string (to be used as part of output file name)
string get_recipient_adr(const string& content) {
    string search_string = "for <";

    // get start of address
    size_t addr_start = content.find(search_string); // try version a
    if (addr_start == string::npos) {
        return ""; // mail does not contain information about the email address of the recipient
    }
    addr_start += search_string.length();

    // get end of address
    size_t addr_end = content.substr(addr_start).find('>');
    if (addr_end == string::npos) {
        return "";
    }

    return content.substr(addr_start, addr_end);
}


/* MAIN FUNCTION */
int main(int argc, char** argv) {

    // data variables
    data *popcl_data = new data;
    BIO *bio;
    SSL *ssl;
    char buf[BUF_SIZE] = {};

    // parse command line options
    try {
        parse_args(argc, argv, popcl_data);
    }
    catch (arg_exception &e) {
        error_exit(popcl_data, nullptr, ARG_ERR, e.what());
    }

    // initialize SSL, BIO library
    SSL_load_error_strings();
    ERR_load_BIO_strings();
    OpenSSL_add_all_algorithms();
    SSL_library_init();

    // if secure protocol is to be used
    if (popcl_data->pop3s or popcl_data->stls) {
        popcl_data->ctx = SSL_CTX_new(SSLv23_client_method());
        // try to load certificates
        // if both '-c' and '-C' options used (certificate file and certificate directory)
        if (!popcl_data->cert_file.empty() and !popcl_data->cert_dir.empty()) {
            // try to load certificates from provided file, non-critical - on error try to load default certificates (then on error exit with POPCL_ERROR)
            if (!SSL_CTX_load_verify_locations(popcl_data->ctx, popcl_data->cert_file.c_str(), popcl_data->cert_dir.c_str())) {
                fprintf(stderr, "popcl - OPENSSL ERROR: cannot load certificates from file provided using '-c' or from directory provided using '-C', using default ones instead\n");
                if (!SSL_CTX_set_default_verify_paths(popcl_data->ctx)) {
                    error_exit(popcl_data, nullptr, OPENSSL_ERR, "popcl - OPENSSL ERROR: error when loading default certificates\n");
                }
            }
        }

        // if '-c' option used (certificate file)
        if (!popcl_data->cert_file.empty()) {
            // try to load certificates from provided file, non-critical - on error try to load default certificates (then on error exit with POPCL_ERROR)
            if (!SSL_CTX_load_verify_locations(popcl_data->ctx, popcl_data->cert_file.c_str(), nullptr)) {
                fprintf(stderr, "popcl - OPENSSL ERROR: cannot load certificates from file provided using '-c', using default ones instead\n");
                if (!SSL_CTX_set_default_verify_paths(popcl_data->ctx)) {
                    error_exit(popcl_data, nullptr, OPENSSL_ERR, "popcl - OPENSSL ERROR: error when loading default certificates\n");
                }
            }
        }
        // if '-C' option used (certificate directory)
        else if (!popcl_data->cert_dir.empty()) {
            // try to load certificates from provided directory, non-critical - on error try to load default certificates (then on error exit with POPCL_ERROR)
            if (!SSL_CTX_load_verify_locations(popcl_data->ctx, popcl_data->cert_file.c_str(), nullptr)) {
                fprintf(stderr, "popcl - OPENSSL ERROR: cannot load certificates from directory provided using '-C', using default ones instead\n");
                if (!SSL_CTX_set_default_verify_paths(popcl_data->ctx)) {
                    error_exit(popcl_data, nullptr, OPENSSL_ERR, "popcl - OPENSSL ERROR: error when loading default certificates\n");
                }
            }
        }
        // no certificate path specified
        else {
            // try to load default certificates
            if (!SSL_CTX_set_default_verify_paths(popcl_data->ctx)) {
                error_exit(popcl_data, nullptr, OPENSSL_ERR, "popcl - OPENSSL ERROR: error when loading default certificates\n");
            }
        }
    }

    // if starting connection through secure protocol
    if (popcl_data->pop3s) {
        // create object for pop3s connection to server
        bio = BIO_new_ssl_connect(popcl_data->ctx);
        BIO_get_ssl(bio, &ssl);
        SSL_set_mode(ssl, SSL_MODE_AUTO_RETRY);
        BIO_set_conn_hostname(bio, (popcl_data->server + ":" + to_string(popcl_data->port)).c_str());
    }
    // else, normal (non secure) protocol
    else {
        // create object for pop3 connection to server
        bio = BIO_new_connect((popcl_data->server + ":" + to_string(popcl_data->port)).c_str());
    }

    // establish connection to server
    if (!bio or (BIO_do_connect(bio) <= 0)){
        error_exit(popcl_data, bio, OPENSSL_ERR, "popcl - OPENSSL ERROR: cannot connect to server\n");
    }

    // get initial response
    pop3_read(popcl_data, bio, buf, true);

    // if '-S', try to upgrade to secure pop3s connection
    if (popcl_data->stls) {
        // execute STLS command on server (ask for connection upgrade)
        if (!pop3_write_and_read(popcl_data, bio, buf, "STLS")) {
            error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: connection upgrade failed\n");
        }

        // upgrade connection object
        // inspired by:
        //      name: OpenSSL: Promote insecure BIO to secure one
        //      date: 11.11.2021
        //      source: https://stackoverflow.com/questions/49132242/openssl-promote-insecure-bio-to-secure-one
        //      question: https://stackoverflow.com/users/4620235/eko
        //      answer: https://stackoverflow.com/users/850848/martin-prikryl
        BIO *ret, *new_ssl;
        // create new secure bio
        if (!(new_ssl = BIO_new_ssl(popcl_data->ctx, 1))) {
            error_exit(popcl_data, bio, OPENSSL_ERR, "popcl - OPENSSL ERROR: connection upgrade failed\n");
        }
        // append to existing bio
        if (!(ret = BIO_push(new_ssl, bio))) {
            error_exit(popcl_data, bio, OPENSSL_ERR, "popcl - OPENSSL ERROR: connection upgrade failed\n");
        }

        // update bio pointer (so it points to the last bio in the chain into which all data will be written)
        bio = ret;
        BIO_get_ssl(bio, &ssl);
        SSL_set_mode(ssl, SSL_MODE_AUTO_RETRY);
    }

    // if secure protocol is to be used
    if (popcl_data->pop3s or popcl_data->stls) {
        // verify certificates
        if(SSL_get_verify_result(ssl) != X509_V_OK) {
            error_exit(popcl_data, bio, OPENSSL_ERR, "popcl - OPENSSL ERROR: certificate verification failed\n");
        }
    }

    // execute authentication - USER and PASS commands
    if (!pop3_write_and_read(popcl_data, bio, buf, "USER " + popcl_data->username)){
        error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: authentication failed\n");
    }
    if (!pop3_write_and_read(popcl_data, bio, buf, "PASS " + popcl_data->password)){
        error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: authentication failed\n");
    }

    // check inbox content - STAT command
    if (!pop3_write_and_read(popcl_data, bio, buf, "STAT")){
        error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: error on stat\n");
    }

    // get number of emails in the inbox
    int number = pop3_get_number(buf);
    if (number == INT_INVALID){
        error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: invalid response format\n");
    }

    int emails_downloaded = 0;
    int emails_deleted = 0;
    int emails_found = number;

    // loop over all emails
    for (int i = 1; i <= number; i++) {
        // check email metadata - LIST command
        if (!pop3_write_and_read(popcl_data, bio, buf, "LIST " + to_string(i))){
            error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR1: error on list (mail " + to_string(i) + ")\n");
        }

        // get email length in bytes
                int length = pop3_get_length(buf, i);
        if (length == INT_INVALID){
            error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: invalid response format\n");
        }

        // start reading email
        if (!pop3_write_and_read(popcl_data, bio, buf, "RETR " + to_string(i))){
            error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: error on read (mail " + to_string(i) + ")\n");
        }

        string content = buf; // content of the whole email

        // strip server response
        size_t pos = content.find("\r\n") + 2;
        content.replace(0, pos, "");

        // subtract number of bytes read from variable indicating expected number of bytes
        length -= content.length();

        // while expecting more data
        while (length > 0) {
            // read another part of email
            if (!pop3_read(popcl_data, bio, buf, false)) {
                error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: error on read (mail " + to_string(i) + ")\n");
            }

            // append read data and subtract from number of expected bytes
            string returned = buf;
            content += returned;
            length -= returned.length();
        }

        // check for position of the actual termination octet indicating end of email and strip it
        size_t ato_pos = content.find("\r\n.\r\n");
        if ((ato_pos + 5) != content.length()) {
            error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: error on read (mail " + to_string(i) + ")\n");
        }
        content.replace(ato_pos, 5, "\r\n");

        // strip byte-stuffed termination octets
        size_t to_pos = 0;
        while ((to_pos = content.find("\r\n.", to_pos)) != std::string::npos) {
            content.replace(to_pos, 3, "\r\n");
            to_pos += 2;
        }


        string msg_id = get_msg_id(content);
        string recipient_addr = get_recipient_adr(content);

        if (recipient_addr.empty()) {
            recipient_addr = popcl_data->username + "@" + popcl_data->server;
        }

        // check and save whether the email is new
        bool is_new = check_msg_id(msg_id, recipient_addr);

        // if email is new or '-n' is not used
        if (is_new or (not popcl_data->msg_new)) {
            // try to save the unique message id of the email if it is new
            if (is_new) {
                save_msg_id(msg_id, recipient_addr);
            }

            // open file for writing and save read email into it
            ofstream file_out;
            file_out.open(popcl_data->out_dir + "/" + to_string(time(nullptr)) + "-" +
                                  recipient_addr + "-" + to_string(i));
            file_out << content;
            file_out.close();

            emails_downloaded++;
        }

        // if delete option used
        if (popcl_data->msg_del) {
            // try to delete message from server, failure is not critical
            if (!pop3_write_and_read(popcl_data, bio, buf, "DELE " + to_string(i))){
                fprintf(stderr, "popcl - POP3 ERROR: deletion failed (mail %i)\n", i);
            } else {
                emails_deleted++;
            }
        }
    }

    // try to terminate connection top server (command QUIT)
    if (!pop3_write_and_read(popcl_data, bio, buf, "QUIT")) {
        error_exit(popcl_data, bio, POPCL_ERR, "popcl - POP3 ERROR: error on quit\n");
    }

    // print information about program results
    if (!popcl_data->msg_new){
        printf("popcl - OK: %i messages downloaded.", emails_downloaded);
    } else {
        printf("popcl - OK: %i new messages downloaded.", emails_downloaded);
    }

    if (popcl_data->msg_del) {
        printf(" %i/%i successfully deleted.", emails_deleted, emails_found);
    }
    printf("\n");

    // free resources
    BIO_free_all(bio);
    if (popcl_data->ctx) {
        SSL_CTX_free(popcl_data->ctx);
    }
    delete popcl_data;

    return POPCL_OK;
}
