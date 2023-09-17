import socket
from time import sleep

host = "192.168.100.10"
port = 9760
addr = (host, port)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(b"Ping", addr)

data = b"Hello!!"
client.sendto(data, addr)
sleep(1)

response = client.recvfrom(9)

passw = b"1947"
client.sendto(passw, addr)
sleep(1)

password_resp = client.recvfrom(10)

if password_resp[0] == b"SUCCESS":
    print("correct pass")
else:
    print("incorrect pass, exit")   

command = b"Read" # Read or Configure
client.sendto(command, addr)

sleep(1)

nop_resp = client.recvfrom(20) # number of pages
print(nop_resp[0], " from ... ", nop_resp)

nop_total = nop_resp[0]

nop = nop_total[16]*2**24 + nop_total[15]*2**16 + nop_total[14]*2**8 + nop_total[13]*2**0

for i in range(nop):
    if(i==0):
        client.recvfrom(10)
    # client.sendto(b"Y", addr)
    # client.recvfrom(10)