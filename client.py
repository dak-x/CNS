# Just for testing to be implemented as a class and to include config

import socket
import toml

UDP_IP = "127.0.0.1"
UDP_PORT = 27012
MESSAGE = b"Hello, World!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
data = sock.recv(1024)

print(data)