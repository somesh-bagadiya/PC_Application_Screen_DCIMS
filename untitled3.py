import os
import time
from datetime import datetime
from threading import Timer

def exitfunc():
    print( "Exit Time", datetime.now())
    print("5 sec over")

Timer(5, exitfunc).start() # exit in 5 seconds

print("Hello")