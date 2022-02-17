"""
File to experiment with threading, and killing subthreads.

Adapted from https://www.geeksforgeeks.org/how-to-use-thread-in-tkinter-python/

"""

import threading as tr
import tkinter as tk
import time

root = tk.Tk()
root.geometry("400x400")

def scan_thread():
    
    # Call the thread here
    t1 = tr.Thread(target=work)
    t1.start()
    
    
def work():
    
    print("Starting the work function.")
    
    for i in range(10):
        print(i)
        time.sleep(1)
    
    print("Work function ended.")
    
# Create Button
tk.Button(root,text="Run",command = scan_thread).pack()

# Execute
root.mainloop()