#!/usr/bin/env python3

import socket
from multiprocessing import Process
import sys

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        print("Proxy serving starting...")
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(2)

        while True:
            conn, addr = server.accept()
            p = Process(target = handle_echo, args = (addr, conn))
            p.daemon = True
            p.start()
            print("Started process", p)

def handle_echo(addr, conn):
    print("Connected by", addr)

    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

if __name__ == "__main__":
    main()
