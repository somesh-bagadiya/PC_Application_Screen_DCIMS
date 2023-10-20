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
configure_bytes = "START:"
date_selected = ""

greenDot = tk.PhotoImage(file="./green.png")
blackDot = tk.PhotoImage(file="./black.png")

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
    
    # root.eval(f'tk::PlaceWindow {str(new)} center')

def configureFunction(timeEnt, dateEnt):
    global configure_bytes
    
    date_selected = str(dateEnt.get_date())
    date_selected = date_selected.split("-")
    date_selected = date_selected[2] + date_selected[1] + date_selected[0][2:]
    
    time = str(timeEnt.get())
    clr = clrVar.get()
    
    if(time == 'HH:MM:SS'):
        messagebox.showerror("Error", "Please enter time")
        return False
    time = time.split(":")
    
    if(int(time[0]) < 24 and int(time[1]) < 60 and int(time[2]) < 60):
        configure_bytes = "START:" + str(time[2]) + str(time[1]) + str(time[0]) + '01' + str(date_selected) + str(clr)
    else:
        messagebox.showerror("Error", "Invalid Time")
    
    print("in configure", configure_bytes)

def configureSection(frame0):
    global configure_bytes, date_selected
        
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
    dateEnt=DateEntry(frame0, selectmode='day')
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

    data_table = [
        ("John Doe", 30, "New York",["John Doe",1,2,3,4,5], 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York","John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),
        ("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),
        ("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),
        ("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),
        ("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),
        ("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),
        ("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),
        ("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),
        ("John Doe", 30, "New York"),
        ("Alice Smith", 25, "Los Angeles"),
        ("Bob Johnson", 35, "Chicago"),
    ]

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
    

def readAndOther(frame1):
    global values
    
    readButton = tk.Button(frame1, text = 'Read', width=10, font=("",10,"bold"), background="#92D050", foreground="white")
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
    if len(password.get()) != 4:
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

# Horizontal scrollbar?
# Time manual input and validation?
# pass is 1947
# unless read is clisked do not alow clear record
# 0a new line char, 09 tab 

# table = tk.Frame(frame1, borderwidth=2, width = 1200, height=400)
# table.grid(column=0, row=1, columnspan=2, sticky='W')
# # table.grid_propagate(0)

# treev = ttk.Treeview(table,  show='tree')
# treev.grid(column=0, row=0)
# # treev.config(width=400)

# style = ttk.Style(table)
# style.theme_use("alt")
# style.configure("Treeview.Heading", background="#A4BEC6", foreground="black")

# verscrlbar = tk.Scrollbar(table, orient ="vertical", command = treev.yview, width=20)
# verscrlbar.grid(column=1, row=0, sticky=tk.N+tk.S)

# horiscrlbar = tk.Scrollbar(table, orient ="horizontal", command = treev.xview, width=20)
# horiscrlbar.grid(column=0, row=1, sticky=tk.W+tk.E)

# treev.configure(yscrollcommand = verscrlbar.set, xscrollcommand = horiscrlbar.set)

# a = list(range(1,25))
# treev["columns"] = a
# treev['show'] = 'headings'

# print(treev["columns"])
# for i in treev["columns"]:
#     treev.column("{}".format(i), minwidth=50, width=60, stretch=0, anchor ='c')
#     treev.heading("{}".format(i), text ="Head {}".format(i))
#     treev.insert("", 'end', text ="L1", values = a) 