from tkinter import *  
import pyvisa
from tkinter.filedialog import asksaveasfile
import Keithley2612B_voltage_sweep as kvs

def save():
    files = [('All Files', '*.*'), ('CSV File', '*.csv'), ('Text Document', '*.txt')]
    file = asksaveasfile (filetypes = files, defaultextension = files)


root = Tk()

# Input Parameters frame
frame_in_par = LabelFrame(root, text = "INPUT PARAMETERS")
frame_in_par.grid()


op_title = StringVar()
op_title.set ('Operator Name:')
op_label = Label (frame_in_par, textvariable = op_title)
op_label.grid(row =0, sticky = 'w')
op_name = StringVar()
op_name_box = Entry (frame_in_par, textvariable = op_name)
op_name_box.grid (row = 0, column = 1, sticky = 'w')

type_title = StringVar()
type_title.set('Select type:')
type_select = Label (frame_in_par, textvariable = type_title)
type_select.grid(row=2, sticky = 'w')
type = StringVar()
type_option_1 = Radiobutton (frame_in_par, text = 'Spin Coated', variable = type, value = 'Spin Coated')
type_option_1.grid(row = 3, sticky = 'w')
type_option_2 = Radiobutton (frame_in_par, text = 'Slot-die small', variable = type, value = 'Slot-die small')
type_option_2.grid(row = 3, column = 1, sticky = 'w')
type_option_3 = Radiobutton (frame_in_par, text = 'Slot-die large', variable = type, value = 'Slot-die large')
type_option_3.grid(row = 4, sticky = 'w')
type_option_4 = Radiobutton (frame_in_par, text = 'Carbon small', variable = type, value = 'Carbon small')
type_option_4.grid(row = 4, column = 1, sticky = 'w')
type_option_5 = Radiobutton (frame_in_par, text = 'Carbon large', variable = type, value = 'Carbon large')
type_option_5.grid(row = 5, sticky = 'w')

measurement_type_title = StringVar()
measurement_type_title.set('Select measurement type:')
measurement_type_select = Label (frame_in_par, textvariable = measurement_type_title)
measurement_type_select.grid(row = 7, sticky = 'w')
measurement_type = StringVar()
measurement_type_option_1 = Radiobutton (frame_in_par, text = 'Normal', variable = measurement_type, value = 'Normal')
measurement_type_option_1.grid(row = 8, sticky = 'w')
measurement_type_option_2 = Radiobutton (frame_in_par, text = 'Thermal Stability', variable = measurement_type, value = 'Thermal Stability')
measurement_type_option_2.grid(row = 9, sticky = 'w')
measurement_type_option_3 = Radiobutton (frame_in_par, text = 'Intensity J-V scans', variable = measurement_type, value = 'Intensity J-V scans')
measurement_type_option_3.grid(row = 10, sticky = 'w')

sample_id_title = StringVar()
sample_id_title.set ('Sample ID:')
sample_id_label = Label (frame_in_par, textvariable = sample_id_title)
sample_id_label.grid(row = 12, sticky = 'w')
sample_id = StringVar()
sample_id_box = Entry (frame_in_par, textvariable = sample_id)
sample_id_box.grid (row = 12, column = 1, sticky = 'w')

min_volt_title = StringVar()
min_volt_title.set ('Min Voltage (V):')
min_volt_label = Label (frame_in_par, textvariable = min_volt_title)
min_volt_label.grid(row = 13, sticky = 'w')
min_volt = StringVar()
min_volt_box = Entry (frame_in_par, textvariable = min_volt)
min_volt_box.grid (row = 13, column = 1, sticky = 'w')

max_volt_title = StringVar()
max_volt_title.set ('Max Voltage (V):')
max_volt_label = Label (frame_in_par, textvariable = max_volt_title)
max_volt_label.grid(row = 14, sticky = 'w')
max_volt = StringVar()
max_volt_box = Entry (frame_in_par, textvariable = max_volt)
max_volt_box.grid (row = 14, column = 1, sticky = 'w')

scan_dir_title = StringVar()
scan_dir_title.set('Scan direction/ Pattern:')
scan_dir_select = Label (frame_in_par, textvariable = scan_dir_title)
scan_dir_select.grid(row = 16, sticky = 'w')
scan_dir = StringVar()
scan_dir_option_1 = Radiobutton (frame_in_par, text = 'Forward', variable = measurement_type, value = 'f')
scan_dir_option_1.grid(row = 17, sticky = 'w')
scan_dir_option_2 = Radiobutton (frame_in_par, text = 'Reverse', variable = measurement_type, value = 'r')
scan_dir_option_2.grid(row = 18, sticky = 'w')
scan_dir_option_3 = Radiobutton (frame_in_par, text = 'Pattern', variable = measurement_type, value = 'p')
scan_dir_option_3.grid(row = 19, sticky = 'w')
pattern = StringVar()
pattern_box = Entry (frame_in_par, textvariable = pattern)
pattern_box.grid (row = 19, column = 1, sticky = 'w')

cell_area_title = StringVar()
cell_area_title.set ('Cell Area (sq. metre):')
cell_area_label = Label (frame_in_par, textvariable = cell_area_title)
cell_area_label.grid(row = 21, sticky = 'w')
cell_area = StringVar()
cell_area_box = Entry (frame_in_par, textvariable = cell_area)
cell_area_box.grid (row = 21, column = 1, sticky = 'w')

scan_rate_title = StringVar()
scan_rate_title.set ('Scan Rate (V/sec):')
scan_rate_label = Label (frame_in_par, textvariable = scan_rate_title)
scan_rate_label.grid(row = 23, sticky = 'w')
scan_rate = StringVar()
scan_rate_box = Entry (frame_in_par, textvariable = scan_rate)
scan_rate_box.grid (row = 23, column = 1, sticky = 'w')

irr_title = StringVar()
irr_title.set ('Irradiance:')
irr_label = Label (frame_in_par, textvariable = irr_title)
irr_label.grid(row = 25, sticky = 'w')
irr = StringVar()
irr_box = Entry (frame_in_par, textvariable = irr)
irr_box.grid (row = 25, column = 1, sticky = 'w')

temp_title = StringVar()
temp_title.set ('Temperature (K):')
temp_label = Label (frame_in_par, textvariable = temp_title)
temp_label.grid(row = 27, sticky = 'w')
temp = StringVar()
temp_box = Entry (frame_in_par, textvariable = temp)
temp_box.grid (row = 27, column = 1, sticky = 'w')

curr_lim_title = StringVar()
curr_lim_title.set ('Crrrent Limit (A):')
curr_lim_label = Label (frame_in_par, textvariable = curr_lim_title)
curr_lim_label.grid(row = 29, sticky = 'w')
curr_lim = StringVar()
curr_lim_box = Entry (frame_in_par, textvariable = curr_lim)
curr_lim_box.grid (row = 29, column = 1, sticky = 'w')

delay_title = StringVar()
delay_title.set ('Delay per scan (sec):')
delay_label = Label (frame_in_par, textvariable = delay_title)
delay_label.grid(row = 31, sticky = 'w')
delay = StringVar()
delay_box = Entry (frame_in_par, textvariable = delay)
delay_box.grid (row = 31, column = 1, sticky = 'w')

file_name_title = StringVar()
file_name_title.set ('File Name:')
file_name_label = Label (frame_in_par, textvariable = file_name_title)
file_name_label.grid(row = 33, sticky = 'w')
file_name = StringVar()
file_name_box = Entry (frame_in_par, textvariable = file_name)
file_name_box.grid (row = 33, column = 1, sticky = 'w')

# Instrument Control frame
ic_frame = LabelFrame(root, text = "INSTRUMENT CONTROL")
ic_frame.grid(row = 0, column = 1, sticky = 'n')
rm = kvs.get_resources()[0]
address_list = kvs.get_resources()[1]

address_select_title = StringVar()
address_select_title.set ('Devices:')
address_select_label = Label (ic_frame, textvariable = address_select_title)
address_select_label.grid(sticky = 'w')

test = ['1', '2', '3']
selected_resc = StringVar()
address_drop = OptionMenu (ic_frame, selected_resc, *test)
address_drop.grid(row = 0, column = 1, sticky = 'w')

#smu = rm.open_resource(selected_resc.get())

def show_status():
    Label (ic_frame, text = f"Connected to: {selected_resc.get()}").grid(row = 1, column = 1)

check_status = Button (ic_frame, text = 'Show Status', command = lambda:show_status())
check_status.grid(row = 1, sticky = 'w')

timeout = StringVar()
timeout_label = Label (ic_frame, text = 'Timeout (sec):').grid(row = 2, sticky = 'w')
timeout_box = Entry (ic_frame, textvariable = timeout)
timeout_box.grid (row = 2, column = 1, sticky = 'w')



# JV Curve frame 
jv_frame = LabelFrame(root, text = "JV CURVE")
k = StringVar()
k.set ('Operator Name:')
kl = Label (jv_frame, textvariable = k)
kl.grid(row =0, sticky = 'w')
jv_frame.grid(row = 0, column = 1, sticky='s')

root.mainloop()

