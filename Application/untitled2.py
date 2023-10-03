# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 12:12:34 2023

@author: ARTRONIFS
"""

from tkinter import ttk
import tkinter as tk
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from datetime import datetime
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image,ImageTk
import socket
# from time import sleep

root = tk.Tk()
root.configure(bg='#DBD9D5')
root.title('PC Application Screen')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# root.state('zoomed')

values = {"Line" : "1", "ADC" : "2", "RTC" : "3", "Flash" : "4", "EEPROM" : "5", "Display" : "6"}
password = tk.StringVar()
clrVar = tk.IntVar()
lineVar = tk.IntVar() 
adcVar = tk.IntVar()
rtcVar = tk.IntVar()
flashVar = tk.IntVar() 
eepromVar = tk.IntVar() 
displayVar = tk.IntVar()
statusArr = [0,0,1,0,1,0]
all_data = []
curr_page_no = 0
status= ""
data_table = []
configure_bytes = ""
board_status = ""
passw = ""
passFlag = ""

greenDot = tk.PhotoImage(file="./green.png")
blackDot = tk.PhotoImage(file="./black.png")

host = "192.168.100.10"
port = 9760
addr = (host, port)


def goHome(new):
    new.destroy()

def channelPage(channelNumber):
    
    new = tk.Toplevel()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print(screen_height, screen_width)
    x = (screen_width-(screen_width/2.5))/2
    y = (screen_height-(screen_height/2.5))/2
    new.configure(bg='#DBD9D5')
    # new.geometry("{}x{}".format(screen_width, screen_height))
    new.state('zoomed')
    # new.columnconfigure(0, weight=1)
    # new.rowconfigure(0, weight=1)
    
    # new = tk.Frame(new, borderwidth=2)
    # new.grid(column=0, row=1, columnspan=2, sticky='NEWS')
    
    homeButton = tk.Button(new, text = 'Home',  font=("",10,"bold"), background="#6FB791", foreground="white", command=lambda: goHome(new))
    homeButton.grid(column=0, row=0, padx=5, sticky="W")
    
    dcimsLabel = ttk.Label(new, text="DCIMS", font=("",15,"bold"), background='#DBD9D5')
    dcimsLabel.grid(column=1, row=0, padx=5)
    f = tkFont.Font(custDetails, custDetails.cget("font"))
    f.configure(underline = True)
    dcimsLabel.configure(font=f)
    
    connFrame = tk.LabelFrame(new, relief="flat", background='#DBD9D5')
    connFrame.grid(column=2, row=0, padx=5, sticky="E")
    connection = ttk.Label(connFrame, text="Connection:", font=("",12,""), background='#DBD9D5')
    connection.grid(column=0, row=0, sticky='E')
    connectionStatus = ttk.Label(connFrame, text=" Live ", font=("",11,""), background="#6FB791", foreground="white", relief="sunken")
    connectionStatus.grid(column=1, row=0, padx=5, pady=5, sticky='W')
    
    chanNumb = ttk.Label(new, text=" CH{} ".format(channelNumber), padding=3, font=("",12,"italic"), background="#9FF961", foreground="#424EBC", relief="groove")
    chanNumb.grid(column=1, row=1)
    
    #-----------------------------------
    
    graph = tk.Frame(new)
    graph.grid(column=0, row=2, columnspan=3, padx=5, pady=5, sticky='W')
    
    graph1 = tk.Frame(graph)
    graph1.grid(column=0, row=1, padx=5, pady=5, sticky='W')
    
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    fig = Figure(figsize = ((screen_width/1.4)*px, (screen_height/3.5)*px), dpi = 100, animated=True)
    y = [1,100,200,500,1000]
    x = ["12 oct","13 oct", "14 oct", "15 oct", "16 oct"]
    fig.tight_layout()
    plot1 = fig.add_subplot(111, xlabel="Date", ylabel="KOhms")
    fig.tight_layout()
    plot1.plot(x,y)
    
    canvas1 = FigureCanvasTkAgg(fig, master=graph1)  
    canvas1.draw()
    canvas1.get_tk_widget().pack()
    
    #-----------------------------------
    
    graph2 = tk.Frame(graph)
    graph2.grid(column=0, row=2, padx=5, pady=5, sticky='W')
    
    fig = Figure(figsize = ((screen_width/1.4)*px, (screen_height/3.5)*px), dpi = 100)
    y = [1,100,50,200,400]
    x = ["12 oct","13 oct", "14 oct", "15 oct", "16 oct"]
    
    plot1 = fig.add_subplot(111, xlabel="Date", ylabel="Volts")
    fig.tight_layout()
    plot1.plot(x,y)
    
    canvas2 = FigureCanvasTkAgg(fig, master=graph2)  
    canvas2.draw()
    canvas2.get_tk_widget().pack()

    now = datetime.now() 
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    datAndTim = ttk.Label(new, text=dt_string, font=("",10,""), background='#DBD9D5')
    datAndTim.grid(column=2, row=5, padx=5, pady=5, sticky='E')
    
    ARTRONIFS = ttk.Label(new, text="Artronifs", font=("",10,"italic"), background='#DBD9D5')
    ARTRONIFS.grid(column=2, row=6, padx=5, pady=5, sticky='E')

def processGonfigFrame(time, date):
    configdata = [0]*14
    configdata[0] = "S"
    configdata[1] = "T"
    configdata[2] = "A"
    configdata[3] = "R"
    configdata[4] = "T"
    configdata[5] = ":"
    
    y = 0
    if(date[0] % 4 == 0):
        y = 64
    for i in range(len(time)):
        x = time[i] % 10
        time[i] = int(time[i]/10)*16 + x
        x = date[i] % 10
        date[i] = int(date[i]/10)*16 + x

    date[1] = date[1] + y
    
    if(clrVar.get()):        
        configdata[13] =  "Y"
    else: 
        configdata[13] = "N"
    
    for i in range(3):
        configdata[6+i] = chr(time[2-i])
        configdata[9] = chr(1)
        configdata[10+i] = chr(date[2-i])

    s = ""
    configdata = bytes(s.join(configdata), 'utf-8')
    return configdata

def configureFunction(timeEnt, dateEnt):
    global configure_bytes, board_status
    date_selected = str(dateEnt.get_date())
    print(date_selected)
    date_selected = date_selected.split("-")
    date_selected[0] = date_selected[0][2:]
    date_selected = [int(i) for i in date_selected]
    
    time = str(timeEnt.get())
    if(time == 'HH:MM:SS'):
        messagebox.showerror("Error", "Please enter time")
        return False
    time = time.split(":")
    time = [int(i) for i in time]
    if(time[0] < 24 and time[1] < 60 and time[2] < 60):
        print(time, date_selected)
        configure_bytes = processGonfigFrame(time, date_selected)
    else:
        messagebox.showerror("Error", "Invalid Time")
    
    # client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # command = b"Configure" # Read or Configure
    # client.sendto(command, addr)
    # send_recv = client.recvfrom(5)
    # print(send_recv)
    # client.sendto(configure_bytes, addr)
    # send_recv = client.recvfrom(20)
    # print(send_recv)
    # client.sendto(b'Exit', addr)
    # status = client.recvfrom(12)
    
    print("in configure", configure_bytes, status)

def configureSection(frame0):
    global configure_bytes
        
    def on_time_entry_click(event):
       if timeEnt.get() == "HH:MM:SS":
          timeEnt.delete(0, tk.END)
          timeEnt.configure(foreground="black")

    def on_time_focus_out(event):
       if timeEnt.get() == "":
          timeEnt.insert(0, "HH:MM:SS")
          timeEnt.configure(foreground="gray")
    
    dateLab = ttk.Label(frame0, text="Date", background='#DBD9D5', font=("",11,"bold"), foreground="#203864")
    dateLab.grid(column=0, row=1, padx=5, pady=5, sticky='W')
    dateEnt=DateEntry(frame0, selectmode='day', date_pattern='dd-MM-yyyy')
    dateEnt.grid(column=1, row=1, padx=5, pady=5, sticky='W')
    
    timeLab = ttk.Label(frame0, text="Time", background='#DBD9D5', font=("",11,"bold"), foreground="#203864")
    timeLab.grid(column=0, row=2, padx=5, pady=5, sticky='W')
    timeEnt=tk.Entry(frame0, width=15, foreground="gray")
    timeEnt.insert(0, 'HH:MM:SS')
    timeEnt.bind("<FocusIn>", on_time_entry_click)
    timeEnt.bind("<FocusOut>", on_time_focus_out)
    timeEnt.grid(column=1, row=2, padx=5, pady=5, sticky='W')
    
    clrRec = tk.Checkbutton(frame0, text="Clear Record", variable=clrVar, background='#DBD9D5', foreground="#203864", font=("",11,"bold"))
    clrRec.grid(column=0, row=5, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)
    
    configButton = tk.Button(frame0, text = 'Configure',  font=("",12,"bold"), background="#92D050", foreground="white", command = lambda : configureFunction(timeEnt, dateEnt))
    configButton.grid(column=0, row=0, columnspan = 2, padx=5, pady=5, sticky=tk.W + tk.E)
    
def statusShow(radioFrame):
    global statusArr
    
    greenImage = Image.open("./green.png")
    greenResize = greenImage.resize((15, 15))
    greenImg = ImageTk.PhotoImage(greenResize)
    
    blackImage = Image.open("./black.png")
    blackResize = blackImage.resize((15, 15))
    blackImg = ImageTk.PhotoImage(blackResize)
    
    a=0
    for i in statusArr:
        if(i==1):
            imgLab = tk.Label(radioFrame, image=greenImg, background='#DBD9D5')
            imgLab.image = greenImg
            imgLab.grid(column=a, row=0, padx=20)
        else:
            imgLab = tk.Label(radioFrame, image=blackImg, background='#DBD9D5')
            imgLab.image = blackImg
            imgLab.grid(column=a, row=0, padx=20)
        a+=1
    
    lineLabel = ttk.Label(radioFrame, text="Line", background='#DBD9D5')
    lineLabel.grid(column=0, row=1)
    
    adcLabel = ttk.Label(radioFrame, text="ADC", background='#DBD9D5')
    adcLabel.grid(column=1, row=1)
    
    rtcLabel = ttk.Label(radioFrame, text="RTC", background='#DBD9D5')
    rtcLabel.grid(column=2, row=1)
    
    flashLabel = ttk.Label(radioFrame, text="Flash", background='#DBD9D5')
    flashLabel.grid(column=3, row=1)
    
    eepromLabel = ttk.Label(radioFrame, text="EEPROM", background='#DBD9D5')
    eepromLabel.grid(column=4, row=1)
    
    displayLabel = ttk.Label(radioFrame, text="Display", background='#DBD9D5')
    displayLabel.grid(column=5, row=1)

def create_table(frame1):
    global data_table
    def on_canvas_configure(event):
        canvas.config(scrollregion=canvas.bbox("all"))

    canvas = tk.Canvas(frame1, width=500)
    canvas.grid(row=0, column=0, sticky="nsew")

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    header_labels = ["Record No", "Date (DDMMYY)", "Time (HH:MIN:SEC)", "Channel Setting", "Channel No", "Impedance P (K-Ohm)", "Impedance N (K-Ohm)", "Voltage (V)", "Channel No", "Impedance P (K-Ohm)", "Impedance N (K-Ohm)", "Voltage (V)", "Channel No", "Impedance P (K-Ohm)", "Impedance N (K-Ohm)", "Voltage (V)", "Channel No", "Impedance P (K-Ohm)", "Impedance N (K-Ohm)", "Voltage (V)", "Channel No", "Impedance P (K-Ohm)", "Impedance N (K-Ohm)", "Voltage (V)"]
    for col, header_text in enumerate(header_labels):
        label = tk.Label(frame, text=header_text, padx=10, pady=5, relief=tk.RIDGE, font=("", 10, "bold"))
        label.grid(row=0, column=col, sticky="nsew")

    for row, row_data in enumerate(data_table, start=1):
        for col, cell_data in enumerate(row_data):
            label = tk.Label(frame, text=cell_data, padx=10, pady=5, relief=tk.RIDGE)
            label.grid(row=row, column=col, sticky="nsew")

    h_scrollbar = tk.Scrollbar(frame1, orient=tk.HORIZONTAL, command=canvas.xview, width=20)
    h_scrollbar.grid(row=1, column=0, sticky="ew")
    canvas.configure(xscrollcommand=h_scrollbar.set)

    v_scrollbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=canvas.yview, width=20)
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=v_scrollbar.set)

    frame.bind("<Configure>", on_canvas_configure)
    for i in range(len(header_labels)):
        frame.grid_columnconfigure(i, weight=1)
    
def processRecords(data, x):
    global data_table
    
    data_record = []
    rec_no = data[x+4]*2**24 + data[x+3]*2**16 + data[x+2]*2**8 + data[x+1]*2**0
    data_record.append(str(rec_no))
    
    sec = int(10*(data[x+6] & 112)/16 + (data[x+6] & 15))
    minu = int(10*(data[x+7] & 112)/16 + (data[x+7] & 15))
    hours = int(10*(data[x+8] & 48)/16 + (data[x+8] & 15))
    day = "Monday" # Hardcoded
    date = int(10*(data[x+10] & 48)/16 + (data[x+10] & 15))
    month = int(10*(data[x+11] & 16)/16 + (data[x+11] & 15))
    year = int(10*(data[x+12] & 240)/16 + (data[x+12] & 15))
    
    date_ddmmyy = str(date) + "/" + str(month) + "/" + str(year)
    data_record.append(date_ddmmyy)
    
    time_hhmmss = str(hours) + ":" + str(minu) + ":" + str(sec)
    data_record.append(time_hhmmss)
    
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
    
    data_record.append(chn_no)
    for i in range(5):
        data_record.append(chn_no[i])
        data_record.append(imp_p[i])
        data_record.append(imp_n[i])
        data_record.append(volt[i])
    
    print(day, ",", date, "/", month, "/", year, "-", hours, ":", minu, ":", sec)
    print("Record No", rec_no)
    print("Channels", chn_no)
    print("Impedance of P", imp_p)
    print("Impedance of n", imp_n)
    print("Voltage", volt)
    print()
    data_table.append(tuple(data_record))

def confirmRecord(data, byt_data, x):
    global buffer
    try:
        if(b'\t' == byt_data[x+5] and b'\t' == byt_data[x+13] and b'\t' == byt_data[x+15]):
            cur_frame_len = countNoOfChannels(x,data)
            data_len = len(byt_data)
            if(cur_frame_len > data_len-x):
                buffer = data[x:]
                processBuffer()
                return False
            return True
        return False
    except:
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

def sendPasswordAndVerify():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(b"Ping", addr)
    data = b"Hello!!"
    client.sendto(data, addr)
    response = client.recvfrom(9)
    
    client.sendto(passw, addr)
    password_resp = client.recvfrom(10)

def readFunction():
    global all_data, curr_page_no, frame1, passw, passFlag
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if(passw==""):
        messagebox.showerror("Error", "Please fill in Password")
        return None
    
    if(passFlag):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        command = b"Read" # Read or Configure
        client.sendto(command, addr)
        nop_resp = client.recvfrom(20) # number of pages
        nop_total = nop_resp[0]
        print(nop_total)
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
        
        readAndOther(frame1)
        
        client.sendto(b'Status?', addr)
        status = client.recvfrom(16)
        print("Status", status)
        
        client.sendto(b'Exit', addr)
        exit_socket = client.recvfrom(12)
        print("Exit", exit_socket)
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(b"Ping", addr)
        data = b"Hello!!"
        client.sendto(data, addr)
        response = client.recvfrom(9)
        
        client.sendto(passw, addr)
        password_resp = client.recvfrom(10)
        
        command = b"Read" # Read or Configure
        client.sendto(command, addr)
        nop_resp = client.recvfrom(20) # number of pages
        nop_total = nop_resp[0]
        print(nop_total)
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
        
        readAndOther(frame1)
        
        client.sendto(b'Status?', addr)
        status = client.recvfrom(16)
        print("Status", status)
        
        client.sendto(b'Exit', addr)
        exit_socket = client.recvfrom(12)
        print("Exit", exit_socket)

def readAndOther(frame1):
    global values
    
    readButton = tk.Button(frame1, text = 'Read', width=10, font=("",10,"bold"), background="#92D050", foreground="white", command=readFunction)
    readButton.grid(column=0, row=0, padx=5, pady=5, sticky="W")
    
    downButton = tk.Button(frame1, text = 'Download', width=10, font=("",10,"bold"), background="#6FB791", foreground="white")
    downButton.grid(column=1, row=0, padx=5, pady=5, sticky="E")
    
    ####################################################################################################
    
    table = tk.Frame(frame1, borderwidth=2)
    table.grid(column=0, row=1, columnspan=2, sticky='WE')
    
    create_table(table)
    
    ####################################################################################################
    
    chnFrame = tk.LabelFrame(frame1, borderwidth=2, background='#DBD9D5', relief="flat")
    chnFrame.grid(column=0, row=3, padx=5, pady=5, columnspan=2)
    
    ch1 = tk.Button(chnFrame, text = 'CH1',  font=("",10,""), command= lambda: channelPage(1), background="#9FF961", foreground="#424EBC")
    ch1.grid(column=0, row=0, padx=23)
    ch2 = tk.Button(chnFrame, text = 'CH2',  font=("",10,""), command= lambda: channelPage(2), background="#9FF961", foreground="#424EBC")
    ch2.grid(column=1, row=0, padx=23)
    ch3 = tk.Button(chnFrame, text = 'CH3',  font=("",10,""), command= lambda: channelPage(3), background="#9FF961", foreground="#424EBC")
    ch3.grid(column=2, row=0, padx=23)
    ch4 = tk.Button(chnFrame, text = 'CH4',  font=("",10,""), command= lambda: channelPage(4), background="#9FF961", foreground="#424EBC")
    ch4.grid(column=3, row=0, padx=23)
    ch5 = tk.Button(chnFrame, text = 'CH5',  font=("",10,""), command= lambda: channelPage(5), background="#9FF961", foreground="#424EBC")
    ch5.grid(column=4, row=0, padx=23)
    
    radioFrame = tk.LabelFrame(frame1, borderwidth=2, background='#DBD9D5', relief="flat")
    radioFrame.grid(column=0, row=4, padx=5, pady=5, columnspan=2)
    
    statusShow(radioFrame)
    
def submitPass():
    global passw, passFlag
    
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(b"Ping", addr)
    data = b"Hello!!"
    client.sendto(data, addr)
    response = client.recvfrom(9)
    print(response)
    if len(password.get()) != 4:
        messagebox.showerror("Error", "Incorrect password")
        password.set("")
    if len(password.get()) == 4:
        passw = str(password.get())
        passw = bytes(passw, 'ascii')
        print(passw)
        client.sendto(passw, addr)
        password_resp = client.recvfrom(10)
        if password_resp[0] == b"SUCCESS":
            print("correct pass")
            passFlag = True
            messagebox.showinfo("Success", "Valid Password")
        else:
            print("incorrect pass, exit")
            passFlag = False
            messagebox.showerror("Error", "Incorrect password")
            password.set("")
        
def on_entry_click(event):
   if passwordEnt.get() == "----":
      passwordEnt.delete(0, tk.END)
      passwordEnt.configure(foreground="white")

def on_focus_out(event):
   if passwordEnt.get() == "":
      passwordEnt.insert(0, "----")
      passwordEnt.configure(foreground="white")        

frame0 = tk.LabelFrame(root, borderwidth=2, background='#DBD9D5')
frame0.grid(column=0, row=1, padx=5, pady=5, sticky='N')

frame1 = tk.LabelFrame(root, borderwidth=2, background='#DBD9D5', width=100)
frame1.grid(column=1, row=1, padx=5, pady=5, columnspan=3, sticky='W')

custDetails = ttk.Label(root, text="DCIMS", font=("",20,"bold"), background='#DBD9D5')
custDetails.grid(column=1, row=0, padx=5, pady=5, sticky='E')
f = tkFont.Font(custDetails, custDetails.cget("font"))
f.configure(underline = True)
custDetails.configure(font=f)

connFrame = tk.LabelFrame(root, relief="flat", background='#DBD9D5')
connFrame.grid(column=3, row=0, padx=5, pady=5, sticky='E')
connection = ttk.Label(connFrame, text="Connection:", font=("",12,"bold"), background='#DBD9D5', foreground="#203864")
connection.grid(column=0, row=0, sticky='E')
connectionStatus = ttk.Label(connFrame, text=" Live ", font=("",11,""), background="#6FB791", foreground="white", relief="sunken")
connectionStatus.grid(column=1, row=0, padx=5, pady=5, sticky='W')

passFrame = tk.LabelFrame(root, relief="flat", background='#DBD9D5')
passFrame.grid(column=0, row=4, padx=5, pady=5, sticky='W')
passLab = ttk.Label(passFrame, text="Password:", background='#DBD9D5', font=("",12,"bold"), foreground="#203864")
passLab.grid(column=0, row=0, sticky='W')
passwordEnt=tk.Entry(passFrame, width=4, background="#BFBFBF", foreground="white", textvariable=password)
passwordEnt.insert(0, '----')
passwordEnt.bind("<FocusIn>", on_entry_click)
passwordEnt.bind("<FocusOut>", on_focus_out)
passwordEnt.grid(column=1, row=0, sticky='W')
submitButton = tk.Button(root, text = 'Submit', width=14, font=("",10,"bold"), background="#6FB791", foreground="white", command=submitPass)
submitButton.grid(column=0, row=5, padx=5, pady=5, sticky="W")

ARTRONIFS = ttk.Label(root, text="Artronifs", font=("",10,"italic"), background='#DBD9D5')
ARTRONIFS.grid(column=0, row=6, padx=5, pady=5, sticky='W')

readAndOther(frame1)    
configureSection(frame0)

root.eval('tk::PlaceWindow . center')
root.mainloop()

# unless read is clisked do not alow clear record
# Add timer in the code
# Status update in the code (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xef\x19\x00\x00', ('192.168.100.10', 9760))
# Plot graph
# Check for eror handling
# Live or dead
# optimization