from tkinter import *  
#import Keithley2612B_voltage_sweep as kvs
root = Tk()

# Input Parameters frame
frame_in_par = LabelFrame(root, text = "INPUT PARAMETERS")
frame_in_par.grid(row = 0, column = 0)
resc_list_labelname = StringVar()
resc_list_label = Label (frame_in_par, textvariable=resc_list_labelname)
resc_list_labelname.set('Operator Name')
resc_list_label.grid(row =0, sticky = 'w')

op_name = StringVar()
op_name_entry = Entry (frame_in_par, textvariable = op_name)
op_name_entry.grid (row = 0, column = 1, sticky = 'w')

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











lb = Label (frame_in_par, textvariable=measurement_type)
lb.grid(row = 11, column=0)




root.mainloop()

print (op_name.get())