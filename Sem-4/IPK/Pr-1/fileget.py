#!/usr/bin/env python3

import socket
import sys
import re
import pathlib

PING_ATTEMPTS = 3
BUFFER_SIZE = 1024
SOCKET_TIMEOUT = 2


# function connects to file server supported in arguments and returns file content of desired file
def get_file_content(file_path, server, fileserver_ip, fileserver_port):
    fs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fs_socket.settimeout(SOCKET_TIMEOUT)
    fs_request = bytes('GET ' + file_path + " FSP/1.0\r\nHostname: " + server + "\r\nAgent: xdudaj02\r\n\r\n", "utf-8")
    fs_address = (fileserver_ip, int(fileserver_port))
    fs_socket.connect(fs_address)

    fs_response = ''
    # loop for repeated attempts to connect when connecting fails
    for ping in range(PING_ATTEMPTS):
        fs_socket.sendto(fs_request, fs_address)
        try:
            fs_response = fs_socket.recv(BUFFER_SIZE).decode('utf-8')
        except socket.timeout:
            sys.stderr.write('FSP: request timed out (' + str(ping + 1) + '/' + str(PING_ATTEMPTS) + ')\n')
            if PING_ATTEMPTS == (ping + 1):
                sys.stderr.write('FSP: request failed\n')
                sys.exit(1)
        else:
            break

    response = re.match(r'^FSP/1.0 (.*)\r', fs_response.split('\n')[0]).group(1)
    length = int(re.match(r'^Length:(\d*)\r', fs_response.split('\n')[1]).group(1))

    fs_data = b''  # variable for file content

    # when only downloading the index file fsp returns both header and data in the first call
    if fs_response.count('\n') > 3:
        fs_data = bytes('\r\n\r\n'.join(fs_response.split('\r\n\r\n')[1:]), 'utf-8')
        length -= len(fs_data)

    # connection not successful
    if response != "Success":
        sys.stderr.write('FSP: ' + response + '\n')
        fs_socket.close()
        sys.exit(1)

    # loop for getting the whole content (when its bigger than BUFFER_SIZE)
    while length > 0:
        try:
            fs_data += fs_socket.recv(min(BUFFER_SIZE, length))
        except socket.timeout:
            sys.stderr.write('FSP: request failed\n')
            fs_socket.close()
            sys.exit(1)
        length -= BUFFER_SIZE
    fs_socket.close()
    return fs_data


# function creates file (or opens if already exists) and writes content (rewrites if file already existed)
def save_file(file_name, content):
    file = open(file_name, "wb")
    file.write(content)
    file.close()


# function used for recreating a file tree, creates all directories in the path of a file if they already dont exist
def create_dirs(file_path):
    dirs = ''.join(('/' + file_path).split('/')[:-1])
    if dirs != "":
        pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)


# main function
def main(argv):
    # argument validity check
    if len(argv) != 5 or "-f" not in argv or "-n" not in argv:
        sys.stderr.write('invalid arguments\n')
        sys.exit(1)

    # argument parsing
    surl = argv[argv.index("-f") + 1]
    nameserver = argv[argv.index("-n") + 1]
    try:
        nameserver_ip, nameserver_port = nameserver.split(":")
    except ValueError:
        sys.stderr.write('invalid arguments\n')
        sys.exit(1)

    # surl validity check
    try:
        server, file_path = re.fullmatch(r'^fsp://((?:\w|-|\.)*)/(.*)$', surl).group(1, 2)
    except AttributeError:
        sys.stderr.write('invalid arguments\n')
        sys.exit(1)

    # name server port validity check
    try:
        nameserver_port = int(nameserver_port)
    except ValueError:
        sys.stderr.write('invalid port\n')
        sys.exit(1)
    if nameserver_port not in range(1, 65535):
        sys.stderr.write('invalid port\n')
        sys.exit(1)

    file_name = surl.split("/")[-1]
    get_all = (file_name == "*")  # true if GET_ALL else false
    if get_all:
        file_path = "index"

    # nsp protocol execution
    ns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ns_socket.settimeout(SOCKET_TIMEOUT)
    ns_request = bytes("WHEREIS " + server, "utf-8")
    ns_address = (nameserver_ip, nameserver_port)

    ns_data = ''
    # loop for repeated attempts to connect when connecting fails
    for ping in range(PING_ATTEMPTS):
        try:
            ns_socket.sendto(ns_request, ns_address)
        except socket.error:
            sys.stderr.write('invalid ip address\n')
            sys.exit(1)
        try:
            ns_data = ns_socket.recv(BUFFER_SIZE).decode('utf-8')
        except socket.timeout:
            sys.stderr.write('NSP: request timed out (' + str(ping + 1) + '/' + str(PING_ATTEMPTS) + ')\n')
            if PING_ATTEMPTS == (ping + 1):
                sys.stderr.write('NSP: request failed\n')
                sys.exit(1)
        else:
            ns_socket.close()
            break

    # nsp response parsing
    status, *response = ns_data.split(' ')
    response = ' '.join(response)
    # connection not successful
    if status != "OK":
        sys.stderr.write('NSP: ' + response + '\n')
        sys.exit(1)
    fileserver_ip, fileserver_port = response.split(':')

    # fsp protocol execution
    content = get_file_content(file_path, server, fileserver_ip, fileserver_port)
    if not get_all:
        save_file(file_name, content)
    else:
        content = content.decode('utf-8').split('\r\n')  # gets list of files to get
        # loops through all files to be downloaded
        for i in content[:-1]:
            file_content = get_file_content(i, server, fileserver_ip, fileserver_port)
            create_dirs(i)
            save_file(i, file_content)


main(sys.argv)
