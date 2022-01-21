#!/usr/bin/env python3

import socket
from multiprocessing import Process
import sys

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

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
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)

                proxy_end.connect((remote_ip, port))

                p = Process(target = handle_proxy, args=(proxy_end, conn))
                p.daemon = True
                p.start
                print("Starting process...", p)




def handle_proxy(proxy_end, conn):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to Google")
    proxy_end.sendall(send_full_data)

    proxy_end.shutdown(socket.SHUT_WR)

    data1 = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending the received data {data1} back to the client")
    conn.send(data1)
    conn.close()

if __name__ == "__main__":
    main()