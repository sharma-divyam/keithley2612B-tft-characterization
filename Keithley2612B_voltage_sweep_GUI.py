from tkinter import *  
import Keithley2612B_voltage_sweep as kvs
root = Tk()

# Resource frame
frame_resc = LabelFrame(root, text = "Resources")
frame_resc.grid(row = 0, column = 0)
resc_list_labelname = StringVar()
resc_list_label = Label (frame_resc, textvariable=resc_list_labelname, anchor= "nw")
resc_list_labelname.set('Available Resources')
resc_list_label.grid(row =0, column = 0)

Lb = Listbox (frame_resc)
Lb.grid(row =  0, column = 1)
items = ['a','b','c','d','e']
for i in range(len(items)):
    Lb.insert (i+1, items[i])


root.mainloop()