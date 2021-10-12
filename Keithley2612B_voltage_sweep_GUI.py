from tkinter import *  
import pyvisa
from tkinter.filedialog import asksaveasfile
import Keithley2612B_voltage_sweep as kvs
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import numpy as np 

def save():
    files = [('All Files', '*.*'), ('CSV File', '*.csv'), ('Text Document', '*.txt')]
    file = asksaveasfile (filetypes = files, defaultextension = files)


root = Tk()
root.title ('Voltage Sweep - Keithley 2612B')
# Input Parameters frame
frame_in_par = LabelFrame(root, text = "INPUT PARAMETERS")
frame_in_par.grid()


op_label = Label (frame_in_par, text = 'Operator Name:')
op_label.grid(row =0, sticky = 'w')
op_name = StringVar()
op_name_box = Entry (frame_in_par, textvariable = op_name)
op_name_box.grid()


type_select = Label (frame_in_par, text = "Select type:")
type_select.grid(row=2, sticky = 'w')
celltype = StringVar()
type_option_1 = Radiobutton (frame_in_par, text = 'Spin Coated', variable = celltype, value = 'Spin Coated')
type_option_1.grid(row = 3, sticky = 'w')
type_option_2 = Radiobutton (frame_in_par, text = 'Slot-die small', variable = celltype, value = 'Slot-die small')
type_option_2.grid(row = 3, column = 1, sticky = 'w')
type_option_3 = Radiobutton (frame_in_par, text = 'Slot-die large', variable = celltype, value = 'Slot-die large')
type_option_3.grid(row = 4, sticky = 'w')
type_option_4 = Radiobutton (frame_in_par, text = 'Carbon small', variable = celltype, value = 'Carbon small')
type_option_4.grid(row = 4, column = 1, sticky = 'w')
type_option_5 = Radiobutton (frame_in_par, text = 'Carbon large', variable = celltype, value = 'Carbon large')
type_option_5.grid(row = 5, sticky = 'w')


measurement_type_select = Label (frame_in_par, text = 'Select measurement type:')
measurement_type_select.grid(row = 7, sticky = 'w')
measurement_type = StringVar()
measurement_type_option_1 = Radiobutton (frame_in_par, text = 'Normal', variable = measurement_type, value = 'Normal')
measurement_type_option_1.grid(row = 8, sticky = 'w')
measurement_type_option_2 = Radiobutton (frame_in_par, text = 'Thermal Stability', variable = measurement_type, value = 'Thermal Stability')
measurement_type_option_2.grid(row = 9, sticky = 'w')
measurement_type_option_3 = Radiobutton (frame_in_par, text = 'Intensity J-V scans', variable = measurement_type, value = 'Intensity J-V scans')
measurement_type_option_3.grid(row = 10, sticky = 'w')


sample_id_label = Label (frame_in_par, text = 'Sample ID:')
sample_id_label.grid(row = 12, sticky = 'w')
sample_id = StringVar()
sample_id_box = Entry (frame_in_par, textvariable = sample_id)
sample_id_box.grid (row = 12, column = 1, sticky = 'w')


min_volt_label = Label (frame_in_par, text = 'Min Voltage (V):')
min_volt_label.grid(row = 13, sticky = 'w')
min_volt = DoubleVar(root,-0.1)
min_volt_box = Entry (frame_in_par, textvariable = min_volt)
min_volt_box.grid (row = 13, column = 1, sticky = 'w')


max_volt_label = Label (frame_in_par, text = 'Max Voltage (V):')
max_volt_label.grid(row = 14, sticky = 'w')
max_volt = DoubleVar(root,1.2)
max_volt_box = Entry (frame_in_par, textvariable = max_volt)
max_volt_box.grid (row = 14, column = 1, sticky = 'w')

steps_no_label = Label (frame_in_par, text = 'Number of steps:')
steps_no_label.grid(row = 15, sticky = 'w')
steps_no = IntVar(root,120)
steps_no_box = Entry (frame_in_par, textvariable = steps_no)
steps_no_box.grid (row = 15, column = 1, sticky = 'w')

def configure_pattern(*args):
    collected_pattern = scan_dir.get()
    print("Collected pattern is: " + collected_pattern)

    if collected_pattern == 'f':
        pattern = 'f'
        print("Reached 83")
        pattern_entry.set('f')
        #pattern_box = Entry (frame_in_par, textvariable = pattern_entry)
        #pattern_box.grid (row = 19, column = 1, sticky = 'w')
        a = 1

    elif collected_pattern == 'r':
        pattern = 'r'
        print("Reached 88")
        pattern_entry.set('r')
        #pattern_box = Entry (frame_in_par, textvariable = pattern_entry)
        #pattern_box.grid (row = 19, column = 1, sticky = 'w')
        a = 2
    else:
        pattern_entry.set("Enter pattern here.")
        #pattern_box = Entry (frame_in_par, textvariable = pattern_entry)
        #pattern_box.grid (row = 19, column = 1, sticky = 'w')
        a = 3
    
    return a
    

scan_dir_select = Label (frame_in_par, text = 'Scan direction/ Pattern:' )
scan_dir_select.grid(row = 16, sticky = 'w')
scan_dir = StringVar()
scan_dir_option_1 = Radiobutton (frame_in_par, text = 'Forward', variable = scan_dir, value = 'f')
scan_dir_option_1.grid(row = 17, sticky = 'w')
scan_dir_option_2 = Radiobutton (frame_in_par, text = 'Reverse', variable = scan_dir, value = 'r')
scan_dir_option_2.grid(row = 18, sticky = 'w')
scan_dir_option_3 = Radiobutton (frame_in_par, text = 'Pattern', variable = scan_dir, value = 'p')
scan_dir_option_3.grid(row = 19, sticky = 'w')
pattern_entry = StringVar(root,"Enter Direction Here.")

# Trace keeps track of the radio button selected. Try this out and check the logs.
scan_dir.trace('w',configure_pattern)

pattern_box = Entry (frame_in_par, textvariable = pattern_entry)
pattern_box.grid (row = 19, column = 1, sticky = 'w')




cell_area_label = Label (frame_in_par, text = 'Cell Area (sq. cm):')
cell_area_label.grid(row = 21, sticky = 'w')
cell_area = DoubleVar(root,0.09)
cell_area_box = Entry (frame_in_par, textvariable = cell_area)
cell_area_box.grid (row = 21, column = 1, sticky = 'w')


scan_rate_label = Label (frame_in_par, text = 'Scan Rate (mV/sec):')
scan_rate_label.grid(row = 23, sticky = 'w')
scan_rate = DoubleVar(root,500)
scan_rate_box = Entry (frame_in_par, textvariable = scan_rate)
scan_rate_box.grid (row = 23, column = 1, sticky = 'w')


irr_label = Label (frame_in_par, text = 'Irradiance:')
irr_label.grid(row = 25, sticky = 'w')
irr = StringVar()
irr_box = Entry (frame_in_par, textvariable = irr)
irr_box.grid (row = 25, column = 1, sticky = 'w')


temp_label = Label (frame_in_par, text = 'Temperature (C):')
temp_label.grid(row = 27, sticky = 'w')
temp = DoubleVar(root, 25)
temp_box = Entry (frame_in_par, textvariable = temp)
temp_box.grid (row = 27, column = 1, sticky = 'w')


curr_lim_label = Label (frame_in_par, text = 'Current Limit (mA):')
curr_lim_label.grid(row = 29, sticky = 'w')
curr_lim = DoubleVar(root,30)
curr_lim_box = Entry (frame_in_par, textvariable = curr_lim)
curr_lim_box.grid (row = 29, column = 1, sticky = 'w')


delay_label = Label (frame_in_par, text = 'NPLC:')
delay_label.grid(row = 31, sticky = 'w')
delay = DoubleVar(root,1)
delay_box = Entry (frame_in_par, textvariable = delay)
delay_box.grid (row = 31, column = 1, sticky = 'w')


file_name_label = Label (frame_in_par, text = 'File Name:')
file_name_label.grid(row = 33, sticky = 'w')
file_name = StringVar()
file_name_box = Entry (frame_in_par, textvariable = file_name)
file_name_box.grid (row = 33, column = 1, sticky = 'w')

# Instrument Control frame
frame_ic = LabelFrame(root, text = "INSTRUMENT CONTROL")
frame_ic.grid(row = 0, column = 1, sticky = 'n')
rm = kvs.get_resources()[0]
address_list = kvs.get_resources()[1]
print(address_list)

address_select_label = Label (frame_ic, text = 'Devices:')
address_select_label.grid(sticky = 'w')

test = ['1', '2', '3']
selected_resc = address_list
address_drop = OptionMenu (frame_ic, selected_resc, *test)
address_drop.grid(row = 0, column = 1, sticky = 'w')

#smu = rm.open_resource(selected_resc)

def show_status():
    Label (frame_ic, text = f"Connected to: {selected_resc}").grid(row = 1, column = 1)

check_status = Button (frame_ic, text = 'Show Status', command = lambda:show_status())
check_status.grid(row = 1, sticky = 'w')

timeout = DoubleVar(root,'30000')
timeout_label = Label (frame_ic, text = 'Timeout (sec):').grid(row = 2, sticky = 'w')
timeout_box = Entry (frame_ic, textvariable = timeout)
timeout_box.grid (row = 2, column = 1, sticky = 'w')

def start ():
    test_output = kvs.sweep_operation(smu, int(steps_no_box.get()), pattern_box.get(), int(delay_box.get()), float(min_volt_box.get()), \
                                    float(max_volt_box.get()), float(scan_rate_box.get()))
    return test_output

start_run = Button (frame_ic, text = 'START RUN', command = lambda:start())
start_run.grid(row = 3, column = 0, sticky = 'w')

stop_run = Button (frame_ic, text = 'STOP RUN')
stop_run.grid(row = 3, column = 1, sticky = 'w')

save_data = Button (frame_ic, text = 'SAVE DATA')
save_data.grid(row = 3, column = 2, sticky = 'w')



# JV Curve frame 

frame_jv = LabelFrame(root, text = "JV CURVE")
frame_jv.grid(row = 0, column = 1, sticky='sw')

def clear_canvas ():
    graph_container = Canvas (frame_jv, height = 400, width = 600, bg = 'white')
    graph_container.grid(row = 1, column = 0)
    fig = Figure(figsize = (6, 4), dpi = 100)
    blank = fig.add_subplot(111)
    blank.set_xlabel('Voltage (mV)')
    blank.set_ylabel('Current Density (mA/sq. cm)')
    blank.set_yticks([0], minor = True)
    blank.yaxis.grid(True)
    blank.xaxis.grid(True)
    canvas = FigureCanvasTkAgg(fig, master = frame_jv)  
    canvas.draw()
    canvas.get_tk_widget().grid(row = 1, column = 0)



clear_canvas()


def plot():
  
    # the figure that will contain the plot
    fig = Figure(figsize = (6, 4), dpi = 100)
  
    x = np.arange (-3,4)
    y = [[-1,0,-4,15,24,10,7], [9,-1,6,7,15,-13,2]]
  
    # adding the subplot
    plot1 = fig.add_subplot(111)
  
    # plotting the graph
    for i in range (len(y)):
        plot1.plot(x,y[i], label = f"y[{i}]")
        plot1.legend(loc='upper left')

    plot1.set_xlabel('Voltage (mV)')
    plot1.set_ylabel('Current Density (mA/sq. cm)')
    plot1.set_yticks([0], minor = True)
    plot1.yaxis.grid(True)
    plot1.xaxis.grid(True)

  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = frame_jv)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row = 1, column = 0)
    """
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame_jv)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().grid(row = 2)
    """

plot_button = Button (frame_jv, text = 'PLOT', command = lambda:plot())
plot_button.grid(row = 0, column = 0)


clear_button = Button (frame_jv, text = 'CLEAR', command = lambda:clear_canvas())
clear_button.grid(row = 0, column = 0, sticky = 'e')

root.mainloop()

