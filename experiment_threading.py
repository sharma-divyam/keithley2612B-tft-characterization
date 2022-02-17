"""
File to experiment with threading, and killing subthreads.

Adapted from https://www.geeksforgeeks.org/how-to-use-thread-in-tkinter-python/

"""

import threading as tr
import tkinter as tk
import time
import signal
from tkinter import Button
import sys

root = tk.Tk()
root.geometry("400x400")




end_event = tr.Event()
kill_event = tr.Event()

buttons = []

def scan_thread():
    
    # Call the thread here
    t1 = tr.Thread(target=work)
    btn1.config(state=tk.DISABLED)
    t1.start()
    
    print(t1.is_alive())
    
    if not t1.is_alive():
        btn1.config(state=tk.NORMAL)
    
def signal_handler(signum, frame):
    end_event.set()
    
def work():
    
    print("Starting the work function.")
    
    for i in range(10):
        print(i)
        
        if end_event.is_set():
            print("Ended.")
            break
        time.sleep(1)
    
    print("Work function ended.")
    return
    
# Create Button

btn1 = Button(root,text="Run",command = lambda: scan_thread())
btn1.pack()

print(btn1)

signal.signal(signal.SIGINT,signal_handler)


# Execute
root.mainloop()