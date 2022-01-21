#!/usr/bin/env python3

import socket
import sys

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# 

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    
    print(f'IP address of {host} is {remote_ip}')
    return remote_ip

def main():
    host = 'www.google.com'
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Proxy serving starting...")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind(HOST, PORT)
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_IP = get_remote_ip(host)
