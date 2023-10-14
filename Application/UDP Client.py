import socket
from time import sleep

host = "127.0.0.1"
port = 4455
addr = (host, port)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    print(socket.getdefaulttimeout())
    print(socket.setdefaulttimeout(1.5))
    print(socket.getdefaulttimeout())
    
    client.sendto(b"Ping", addr)
    
    data = b"!EXIT!"
    sleep(2)
    data = b"!EXIT!"
    client.sendto(data, addr)
    print(client.recvfrom(10))
    print(client.recvfrom(10))
    print(client.recvfrom(10))
except TimeoutError:
    print("Timed out error")
