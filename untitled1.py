import socket
from time import sleep

def processRecords(data, x):
    
    rec_no = data[x+4]*2**24 + data[x+3]*2**16 + data[x+2]*2**8 + data[x+1]*2**0
    
    sec = int(10*(data[x+6] & 112)/16 + (data[x+6] & 15))
    minu = int(10*(data[x+7] & 112)/16 + (data[x+7] & 15))
    hours = int(10*(data[x+8] & 48)/16 + (data[x+8] & 15))
    day = "Monday" # Hardcoded
    date = int(10*(data[x+10] & 48)/16 + (data[x+10] & 15))
    month = int(10*(data[x+11] & 16)/16 + (data[x+11] & 15))
    year = int(10*(data[x+12] & 240)/16 + (data[x+12] & 15))
    
    chn_no = []
    imp_p = []
    imp_n = []
    volt = []
    chn_act = bin(data[x+14])[2:]
    chn_act = chn_act[::-1]
    i = x+16
    for j in range(len(chn_act)):
        if(chn_act[j] == "1"):
            chn_no.append(data[i])
            imp_p.append(data[i+4]*2**24 + data[i+3]*2**16 + data[i+2]*2**8 + data[i+1]*2**0)
            imp_n.append(data[i+8]*2**24 + data[i+7]*2**16 + data[i+6]*2**8 + data[1+5]*2**0)
            volt.append(data[i+10]*2**8 + data[i+9]*2**0)
            i+=12
        else:
            chn_no.append("NA")
            imp_p.append("NA")
            imp_n.append("NA")
            volt.append("NA")
            i+=1
        
    print(day, ",", date, "/", month, "/", year, "-", hours, ":", minu, ":", sec)
    print("Record No", rec_no)
    print("Channels", chn_no)
    print("Impedance of P", imp_p)
    print("Impedance of n", imp_n)
    print("Voltage", volt)
    print()

def confirmRecord(data, byt_data, x):
    global buffer
    if(b'\t' == byt_data[x+5] and b'\t' == byt_data[x+13] and b'\t' == byt_data[x+15]):
        cur_frame_len = countNoOfChannels(x,data)
        data_len = len(byt_data)
        if(cur_frame_len > data_len-x):
            buffer = data[x:]
            processBuffer()
            return False
        return True
    return False

def countNoOfChannels(x,data):
    chn_act = bin(data[x+14])[2:]
    count=16
    for i in range(len(chn_act)):
        if(chn_act[i] == "1"):
            count+=12
        else:
            count+=1
    return count

def processBuffer():
    global buffer, curr_page_no, all_data
    buffer_data = []
    i = 0
    try:
        buffer_data = list(all_data[curr_page_no+1])
    except IndexError:
        print("out of pages")
        return False
    byt_data_new = [bytes([b]) for b in buffer_data]
    if(buffer!=""):
        for i in range(len(byt_data_new)):
            if b'\n' == byt_data_new[i]:
                break
            
        buffer = list(buffer) + list(buffer_data[:i])
        cur_frame_len_ideal = countNoOfChannels(0,buffer)
        print(cur_frame_len_ideal, len(buffer))
        
        if(cur_frame_len_ideal == len(buffer)):
            processRecords(buffer, 0)
            print("Processed buffer")
        else:
            print("buffer discarded")
            buffer = ""
            return False
            
        buffer = ""

def processData(data, flag):
    global buffer
    if(flag):
        data = data[6:]
    
    frame_size = []
    byt_data = [bytes([b]) for b in data]
    
    for i in range(len(byt_data)):
        if b'\n' == byt_data[i]:
            frame_size.append(i)

    for i in frame_size:
        rec_flag = confirmRecord(data, byt_data, i)
        if(rec_flag):
            processRecords(data, i)
        else:
            continue

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
all_data = []
for i in range(nop+1): # +1 for END
    client.sendto(b"Y", addr)
    data = client.recvfrom(262)
    data = data[0]
    all_data.append(data)

for i in range(len(all_data)):
    data = all_data[i]
    curr_page_no = i
    if(i==0):
        processData(data, True)
    else:
        processData(data, False)

client.sendto(b'Status?', addr)
status = client.recvfrom(16)

client.sendto(b'Exit', addr)
status = client.recvfrom(12)

# buffer = ""
# # data = b'START:\n\x00\x00\x00\x00\t\x88 #)0\x08#\t\x1b\t\x01Ln\x00\x00Ln\x00\x00Mn\t\x02\x00\x00Mn\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00dn\x00\x00\x04\x05\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x88%#)0\x08#\t\x1b\t\x01In\x00\x00In\x00\x00Jn\t\x02\x00\x00Jn\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00`n\x00\x00A\x05\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x880#)0\x08#\t\x1b\t\x01Hn\x00\x00Hn\x00\x00[n\t\x02\x00\x00[n\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00Wn\x00\x00\x03\x05\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x885#)0\x08#\t\x1b\t\x01Fn\x00\x00Fn\x00\x00]n\t\x02\x00\x00]n\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00Fn\x00\x00\x97\x04\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad'
# all_data = [b'START:\n\x00\x00\x00\x00\t\x88 #)0\x08#\t\x1b\t\x01Ln\x00\x00Ln\x00\x00Mn\t\x02\x00\x00Mn\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00dn\x00\x00\x04\x05\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x88%#)0\x08#\t\x1b\t\x01In\x00\x00In\x00\x00Jn\t\x02\x00\x00Jn\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00`n\x00\x00A\x05\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x880#)0\x08#\t\x1b\t\x01Hn\x00\x00Hn\x00\x00[n\t\x02\x00\x00[n\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00Wn\x00\x00\x03\x05\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x885#)0\x08#\t\x1b\t\x01Fn\x00\x00Fn\x00\x00]n\t\x02\x00\x00]n\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00Fn\x00\x00\x97\x04\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad',b'\x01\xad\x01\t\n\x00\x00\x00\x00\t\x88@#)0\x08#\t\x1b\t\x01Bn\x00\x00Bn\x00\x00[n\t\x02\x00\x00!\x06\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00\xca\x04\x00\x00Cn\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x88E#)0\x08#\t\x1b\t\x01?n\x00\x00?n\x00\x00Yn\t\x02\x00\x00\xcb\x04\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00=\x04\x00\x00An\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xad\x01\xad\x01\t\n\x00\x00\x00\x00\t\x88P#)0\x08#\t\x1b\t\x01?n\x00\x00?n\x00\x00Wn\t\x02\x00\x00\xcb\x04\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00\x1f7\x00\x00?n\x00\x00\t\x05\xad\x01\xad\x01\x00\x00\xac\x01\xad\x01\t\n\x00\x00\x00\x00\t\x88U#)0\x08#\t\x1b\t\x01=n\x00\x00=n\x00\x00Wn\t\x02\x00\x00\x98\x04\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x00=n\x00\x00=n\x00\x00\t\x05\xac\x01\xad',b'\n\x00\x00\x00\x00\t\x88)\x01)1\x08#\t\x18\t\t\t\t\x04\x00\x009n\x00\x009n\x00\x00\t\x05\x00\x00\x00\x00\x00\x00\xad\x01\xac\x01\t\n\x00\x00\x00\x00\t\xd79\x01)1\x08#\t\x18\t\t\t\t\x04\x00\x007n\x00\x007n\x00\x00\t\x05\x00\x00\x00\x00\x00\x00\xad\x01\xac\x01\t\n\x00\x00\x00\x00\t\x81E\x01)1\x08#\t\x1b\t\x01Kn\x00\x00Kn\x00\x003n\t\x02\x00\x003n\x00\x00\xe8\x03\x00\x00\t\t\x04\x00\x002n\x00\x002n\x00\x00\t\x05\xad\x01\xac\x01\x00\x00\xac\x01\xac\x01\t\n\x00\x00\x00\x00\t\x80Q\x01)1\x08#\t\x1f\t\x01/n\x00\x00/n\x00\x00>\x05\t\x02\x00\x00.n\x00\x00Dn\x00\x00\t\x03Dn\x00\x00/n\x00\x00>\x05\t\x04\x00\x00/n\x00\x00/n\x00\x00\t\x05\xac\x01\xac\x01\xad\x01\xac\x01\xac\x01\t\n\x00\x00\x00\x00\t\x80W\x01)1\x08#\t\x1f\t\x01Fn\x00\x00Fn\x00\x00/n\t\x02',b"\x00\x00/n\x00\x00.n\x00\x00\t\x03.n\x00\x00,n\x00\x00\x08\x16\t\x04\x00\x00\x96\x04\x00\x000n\x00\x00\t\x05\xad\x01\xac\x01\xac\x01\xac\x01\xac\x01\t\n\x00\x00\x00\x00\t\x80\x03\x02)1\x08#\t\x1f\t\x01,n\x00\x00,n\x00\x00+n\t\x02\x00\x00+n\x00\x00\xc9\x04\x00\x00\t\x03,n\x00\x00En\x00\x00En\t\x04\x00\x00/n\x00\x00/n\x00\x00\t\x05\xac\x01\xac\x01\xac\x01\xad\x01\xac\x01\t\n\x00\x00\x00\x00\t\x80\t\x02)1\x08#\t\x1f\t\x01+n\x00\x00+n\x00\x00Cn\t\x02\x00\x00Cn\x00\x00(n\x00\x00\t\x03(n\x00\x00*n\x00\x00\x03\x0b\t\x04\x00\x00+n\x00\x00+n\x00\x00\t\x05\xac\x01\xad\x01\xac\x01\xac\x01\xac\x01\t\n\x00\x00\x00\x00\t\x80\x15\x02)1\x08#\t\x1f\t\x01'n\x00\x00'n\x00\x00'n\t\x02\x00\x00\xe2\x06\x00\x00%n\x00\x00\t\x03\x96\x04\x00\x00\x01\x05\x00\x00(n\t\x04\x00\x00An"]
# for i in range(len(all_data)):
#     curr_page_no = i
#     print("Current page Number",curr_page_no)
#     data = list(all_data[i])
#     if(i==0):
#         processData(data, True)
#     else:
#         processData(data, False)

# error hanbling for index error 
# check upto 3 
# add more conditions for new record check