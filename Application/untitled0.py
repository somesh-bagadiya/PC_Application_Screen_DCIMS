# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 12:08:44 2023

@author: somes
"""

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

nop_total = nop_resp[0]

nop = nop_total[16]*2**24 + nop_total[15]*2**16 + nop_total[14]*2**8 + nop_total[13]*2**0
print(nop)
for i in range(nop+1): # +1 for END
    client.sendto(b"Y", addr)
    if(i==0):
        data1 = client.recvfrom(262)
        print(data1)
    else:        
        data = client.recvfrom(262)
        print(data)

# volt = a[32]*2**8 + a[31]*2**0
# imp_n = a[30]*2*24 + a[29]*2**16 + a[28]*2**8 + a[27]*2**0
# imp_p = a[26]*2*24 + a[25]*2**16 + a[24]*2**8 + a[23]*2**0
# a[22] channel no
# bin(a[20])[2:] conver to binary for channel info
# (a[18] & 15) + 10*(a[18] & 240)/16 # year
# (a[17] & 15) + 10*(a[17] & 16)/16 # month
# (a[16] & 15) + 10*(a[16]& 48)/16 # date
# (a[15] & 15) + 10*(a[15]& 48)/16 # day which is always 1 can ignore
# (a[14] & 15) + 10*(a[14]& 48)/16 # hours
# (a[13] & 15) + 10*(a[13]& 112)/16 # min
# (a[12] & 15) + 10*(a[12]& 112)/16 # sec
# rec_no = a[10]*2*24 + a[9]*2**16 + a[8]*2**8 + a[7]*2**0

# b'START:\n\x00\x00\x00\x00\t\x88 #)0\x08#\t\x1b\t\x01Ln\x00\x00Ln\x00\x00Mn\t\x02\x00\x00Mn\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00dn\x00\x00\x04\x05\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x88%#)0\x08#\t\x1b\t\x01In\x00\x00In\x00\x00Jn\t\x02\x00\x00Jn\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00`n\x00\x00A\x05\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x880#)0\x08#\t\x1b\t\x01Hn\x00\x00Hn\x00\x00[n\t\x02\x00\x00[n\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00Wn\x00\x00\x03\x05\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x885#)0\x08#\t\x1b\t\x01Fn\x00\x00Fn\x00\x00]n\t\x02\x00\x00]n\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00Fn\x00\x00\x97\x04\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad'