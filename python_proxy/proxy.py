# encoding:utf-8

import _thread
import socket
import sys
import traceback

from utils import print_ext


# how many pending connections queue will hold
MAX_CONNECTIONS = 50
# max number of bytes we receive at once
MAX_DATA_RECEIVE = 999999
# set to True to see the debug msgs
DEBUG = True
# just an example. Remove with [""] for no blocking at all.
BLOCKED_URLS = []


def main():
    # check the length of command running
    if len(sys.argv) < 2:
        print_ext("no port is given, using :8080 (http-default)")
        port = 8080
    else:
        # port from argument
        port = int(sys.argv[1])

    # host and port info.
    # blank for localhost
    host = 'localhost'
    print_ext("proxy server running on %s with port %s" % (host, port))

    try:
        # create a socket
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # associate the socket to host and port
        proxy_socket.bind((host, port))
        # listening
        proxy_socket.listen(MAX_CONNECTIONS)

    except socket.error:
        print_ext(traceback.format_exc())
        sys.exit(1)

    # get the connection from client
    while True:
        conn, client_address = proxy_socket.accept()

        # create a thread to handle request
        _thread.start_new_thread(proxy_thread, (conn,))


def proxy_thread(conn):
    # get the request from browser
    request = str(conn.recv(MAX_DATA_RECEIVE))

    # parse the first line
    first_line = request.split('\n')[0]

    # get url
    url = first_line.split(' ')[1]

    print_ext("got url is: %s" % url)

    if url in BLOCKED_URLS:
        print_ext("url: %s is blocked" % url)
        conn.close()
        return

    # url: beacons5.gvt2.com:443
    # url: http://www.liaoxuefeng.com/
    try:
        port = int(url.rsplit(":")[-1].strip())
        domain_name = url.rsplit(":")[0].strip()
    except ValueError:
        port = 80
        domain_name = url.split("://www.")[-1].rsplit("/")[0]

    print_ext("domain name: %s, port: %s" % (domain_name, port))

    try:
        # create a socket to connect to the web server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((domain_name, port))
        # send request to web server
        server_socket.send(request.encode('utf-8'))

        while True:
            # receive data from web server
            data = server_socket.recv(MAX_DATA_RECEIVE)

            if len(data) > 0:
                # send to browser
                conn.send(data)
            else:
                break
        server_socket.close()
        conn.close()
    except socket.error:
        print_ext(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
