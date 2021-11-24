
import tkinter as tk
import pyvisa
import tkinter.filedialog
import Keithley2612B_voltage_sweep as kvs
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import numpy as np 
from time import sleep
import pandas as pd
import seaborn as sns

class Application(tk.Tk):

    def __init__(self):

        # Declaration of self is required for all object variables and object methods, because of python.

        super().__init__()
        
        # Define the object variables. These variables will be shared (i.e. 'global') within the defined objects.
        # Functions in objects have full access to the object variables, so we can call a function, and return its output to one of these variables.
        # That way, data collected from the scan can be transferred to another function (the plot())

        # Since the canvas and matplotlib fig (and axes) will remain the same, I have declared them as object variables instead. 
        # Likewise, the connection to the smu is made in this py file, but the start() requires it as well, so I declared it as an object variable.

        self.dict_data = None
        self.address_list = None
        self.directory = None
        self.fig = None
        self.smu = None
        self.rm = None
        self.multidelay = None
        self.canvas = None
        self.plot1 = None
        self.graph_container = None

        # Define the layout
        self.title('Voltage Sweep - Keithley 2612B')

        # Input Parameters frame
        self.frame_in_par = tk.LabelFrame(self, text = "INPUT PARAMETERS")
        self.frame_in_par.grid()

        # Operator Name
        self.op_label = tk.Label (self.frame_in_par, text = 'Operator Name:')
        self.op_label.grid(row =0, sticky = 'w')
        self.op_name = tk.StringVar(self,"Name")
        self.op_name_box = tk.Entry (self.frame_in_par, textvariable = self.op_name)
        self.op_name_box.grid()

        # Cell Type
        self.type_select = tk.Label (self.frame_in_par, text = "Select type:")
        self.type_select.grid(row=2, sticky = 'w')
        self.celltype = tk.StringVar()
        self.type_option_1 = tk.Radiobutton (self.frame_in_par, text = 'Spin Coated', variable = self.celltype, value = 'Spin Coated',tristatevalue='x')
        self.type_option_1.grid(row = 3, sticky = 'w')
        self.type_option_2 = tk.Radiobutton (self.frame_in_par, text = 'Slot-die small', variable = self.celltype, value = 'Slot-die small',tristatevalue='x')
        self.type_option_2.grid(row = 3, column = 1, sticky = 'w')
        self.type_option_3 = tk.Radiobutton (self.frame_in_par, text = 'Slot-die large', variable = self.celltype, value = 'Slot-die large',tristatevalue='x')
        self.type_option_3.grid(row = 4, sticky = 'w')
        self.type_option_4 = tk.Radiobutton (self.frame_in_par, text = 'Carbon small', variable = self.celltype, value = 'Carbon small',tristatevalue='x')
        self.type_option_4.grid(row = 4, column = 1, sticky = 'w')
        self.type_option_5 = tk.Radiobutton (self.frame_in_par, text = 'Carbon large', variable = self.celltype, value = 'Carbon large',tristatevalue='x')
        self.type_option_5.grid(row = 5, sticky = 'w')

        self.celltype.trace('w',self.showCellType)

        # Measurement Type
        self.measurement_type_select = tk.Label (self.frame_in_par, text = 'Select measurement type:')
        self.measurement_type_select.grid(row = 7, sticky = 'w')
        self.measurement_type = tk.StringVar()
        self.measurement_type_option_1 = tk.Radiobutton (self.frame_in_par, text = 'Normal', variable = self.measurement_type, value = 'Normal',tristatevalue='x')
        self.measurement_type_option_1.grid(row = 8, sticky = 'w')
        self.measurement_type_option_2 = tk.Radiobutton (self.frame_in_par, text = 'Thermal Stability', variable = self.measurement_type, value = 'Thermal Stability',tristatevalue='x')
        self.measurement_type_option_2.grid(row = 9, sticky = 'w')
        self.measurement_type_option_3 = tk.Radiobutton (self.frame_in_par, text = 'Intensity J-V scans', variable = self.measurement_type, value = 'Intensity J-V scans',tristatevalue='x')
        self.measurement_type_option_3.grid(row = 10, sticky = 'w')

        self.measurement_type.trace('w',self.showMeasurementType)

        # Sample_ID
        self.sample_id_label = tk.Label (self.frame_in_par, text = 'Sample ID:')
        self.sample_id_label.grid(row = 12, sticky = 'w')
        self.sample_id = tk.StringVar(self,"Example: 1-1")
        self.sample_id_box = tk.Entry (self.frame_in_par, textvariable = self.sample_id)
        self.sample_id_box.grid (row = 12, column = 1, sticky = 'w')

        # Min Voltage
        self.min_volt_label = tk.Label (self.frame_in_par, text = 'Min Voltage (V):')
        self.min_volt_label.grid(row = 13, sticky = 'w')
        self.min_volt = tk.DoubleVar(self,-0.1)
        self.min_volt_box = tk.Entry (self.frame_in_par, textvariable = self.min_volt)
        self.min_volt_box.grid (row = 13, column = 1, sticky = 'w')

        # Max Voltage
        self.max_volt_label = tk.Label (self.frame_in_par, text = 'Max Voltage (V):')
        self.max_volt_label.grid(row = 14, sticky = 'w')
        self.max_volt = tk.DoubleVar(self,1.2)
        self.max_volt_box = tk.Entry (self.frame_in_par, textvariable = self.max_volt)
        self.max_volt_box.grid (row = 14, column = 1, sticky = 'w')

        # Number of steps
        self.steps_no_label = tk.Label (self.frame_in_par, text = 'Number of steps:')
        self.steps_no_label.grid(row = 15, sticky = 'w')
        self.steps_no = tk.IntVar(self,120)
        self.steps_no_box = tk.Entry (self.frame_in_par, textvariable = self.steps_no)
        self.steps_no_box.grid (row = 15, column = 1, sticky = 'w')

        # Scan direction
        self.scan_dir_select = tk.Label (self.frame_in_par, text = 'Scan direction/ Pattern:' )
        self.scan_dir_select.grid(row = 16, sticky = 'w')
        self.scan_dir = tk.StringVar()
        self.scan_dir_option_1 = tk.Radiobutton (self.frame_in_par, text = 'Forward', variable = self.scan_dir, value = 'f',tristatevalue='x')
        self.scan_dir_option_1.grid(row = 17, sticky = 'w')
        self.scan_dir_option_2 = tk.Radiobutton (self.frame_in_par, text = 'Reverse', variable = self.scan_dir, value = 'r',tristatevalue='x')
        self.scan_dir_option_2.grid(row = 18, sticky = 'w')
        self.scan_dir_option_3 = tk.Radiobutton (self.frame_in_par, text = 'Pattern', variable = self.scan_dir, value = 'p',tristatevalue='x')
        self.scan_dir_option_3.grid(row = 19, sticky = 'w')
        self.pattern_entry = tk.StringVar(self,"Enter Direction Here.")

        # Trace keeps track of the radio button selected. Try this out and check the logs.
        self.scan_dir.trace('w',self.configure_pattern)


        self.pattern_box = tk.Entry (self.frame_in_par, textvariable = self.pattern_entry)
        self.pattern_box.grid (row = 19, column = 1, sticky = 'w')


        # Cell Area
        self.cell_area_label = tk.Label (self.frame_in_par, text = 'Cell Area (sq. cm):')
        self.cell_area_label.grid(row = 21, sticky = 'w')
        self.cell_area = tk.DoubleVar(self,0.09)
        self.cell_area_box = tk.Entry (self.frame_in_par, textvariable = self.cell_area)
        self.cell_area_box.grid (row = 21, column = 1, sticky = 'w')

        # Scan Rate
        self.scan_rate_label = tk.Label (self.frame_in_par, text = 'Scan Rate (mV/sec):')
        self.scan_rate_label.grid(row = 23, sticky = 'w')
        self.scan_rate = tk.DoubleVar(self,500)
        self.scan_rate_box = tk.Entry (self.frame_in_par, textvariable = self.scan_rate)
        self.scan_rate_box.grid (row = 23, column = 1, sticky = 'w')

        # Irradiance
        self.irr_label = tk.Label (self.frame_in_par, text = 'Irradiance (Suns):')
        self.irr_label.grid(row = 25, sticky = 'w')
        self.irr = tk.DoubleVar(self, 1)
        self.irr_box = tk.Entry (self.frame_in_par, textvariable = self.irr)
        self.irr_box.grid (row = 25, column = 1, sticky = 'w')

        # Temperature
        self.temp_label = tk.Label (self.frame_in_par, text = 'Temperature (C):')
        self.temp_label.grid(row = 27, sticky = 'w')
        self.temp = tk.DoubleVar(self, 25)
        self.temp_box = tk.Entry (self.frame_in_par, textvariable = self.temp)
        self.temp_box.grid (row = 27, column = 1, sticky = 'w')

        # Current compliance
        self.curr_lim_label = tk.Label (self.frame_in_par, text = 'Current Limit (mA):')
        self.curr_lim_label.grid(row = 29, sticky = 'w')
        self.curr_lim = tk.DoubleVar(self,30)
        self.curr_lim_box = tk.Entry (self.frame_in_par, textvariable = self.curr_lim)
        self.curr_lim_box.grid (row = 29, column = 1, sticky = 'w')

        # NPLC DELAY 
        self.delay_label = tk.Label (self.frame_in_par, text = 'NPLC:')
        self.delay_label.grid(row = 31, sticky = 'w')
        self.delay = tk.DoubleVar(self,1)
        self.delay_box = tk.Entry (self.frame_in_par, textvariable = self.delay)
        self.delay_box.grid (row = 31, column = 1, sticky = 'w')

        # DELAY PER SCAN (FOR MULTIPLE SCANS) 
        self.multidelay_label = tk.Label (self.frame_in_par, text = 'Delay per scan (s):')
        self.multidelay_label.grid(row = 32, sticky = 'w')
        self.multidelay = tk.DoubleVar(self,0)
        self.multidelay_box = tk.Entry (self.frame_in_par, textvariable = self.multidelay)
        self.multidelay_box.grid (row = 32, column = 1, sticky = 'w')

        # Directory. I changed it to a button to choose the directory. 
        # Auto-saving of data is preferred, and it saves time with the whole scanning process
        # For the same reason in the Keithley py file, the filename is automatically created. 
        self.savedir = tk.Button (self.frame_in_par, text = 'Choose Save Location', command = lambda: self.getDirectory())
        self.savedir.grid(row = 33, sticky = 'w')
        self.directory_fill = tk.StringVar()
        self.directory_box = tk.Entry (self.frame_in_par, textvariable = self.directory_fill)
        self.directory_box.grid (row = 33, column = 1, sticky = 'w')
        self.directory_fill.trace('w',self.directory_fill_setter)

        #self.clear_button = Button (self.frame_jv, text = 'CLEAR', command = lambda:self.clear_canvas())
        #self.clear_button.grid(row = 0, column = 0, sticky = 'e')

        # Instrument Control frame
        self.frame_ic = tk.LabelFrame(self, text = "INSTRUMENT CONTROL")
        self.frame_ic.grid(row = 0, column = 1, sticky = 'n')
        
        # PyVisa set-up.
        # I chose to make the ResourceManager an object variable as well, so that the actual connection,
        # which is done by another function (selectResource()), need not declare a new ResourceManager just to make the connection.
        # This code will fail if no devices are detected. 

        self.rm = pyvisa.ResourceManager()
        self.address_list = list(self.rm.list_resources()) # list_resources() gives a tuple, I converted it to a list.
        print("Address list: " + str(self.address_list))

        self.address_select_label = tk.Label (self.frame_ic, text = 'Devices:')
        self.address_select_label.grid(sticky = 'w')

        # selected_resc will change when an option in the OptionMenu is clicked. This click is tracked by the trace function below.
        self.selected_resc = tk.StringVar()
        self.address_drop = tk.OptionMenu (self.frame_ic, self.selected_resc, *self.address_list)
        self.address_drop.grid(row = 0, column = 1, sticky = 'w')
        
        self.selected_resc.trace('w',self.selectResource)        

        # Check status button
        self.check_status = tk.Button (self.frame_ic, text = 'Show Status', command = lambda: self.show_status())
        self.check_status.grid(row = 1, sticky = 'w')

        self.timeout = tk.DoubleVar(self,30000)
        self.timeout_label = tk.Label (self.frame_ic, text = 'Timeout (sec):').grid(row = 2, sticky = 'w')
        self.timeout_box = tk.Entry (self.frame_ic, textvariable = self.timeout)
        self.timeout_box.grid (row = 2, column = 1, sticky = 'w')


        # Buttons for starting and stopping
        self.start_run = tk.Button (self.frame_ic, text = 'START RUN', command =lambda:(self.start()))
        self.start_run.grid(row = 3, column = 0, sticky = 'w')

        self.stop_run = tk.Button (self.frame_ic, text = 'STOP RUN',command = lambda:(self.stop()))
        self.stop_run.grid(row = 3, column = 2, sticky = 'w')

        #self.save_data = Button (self.frame_ic, text = 'SAVE DATA')
        #self.save_data.grid(row = 3, column = 2, sticky = 'w')
    
        
        # JV Curve frame 
        self.frame_jv = tk.LabelFrame(self, text = "JV CURVE")
        self.frame_jv.grid(row = 0, column = 1, sticky='sw')
        self.canvas = self.clear_canvas()

        # Removed the ones below.
        # When we scan, we expect that the graphs show immediately, and on starting the next scan, the screen is cleared and 
        # immediately ready for the next scan.
        # This is to make this program as similar as the one we are currently using. 

        #self.clear_button = tk.Button (self.frame_jv, text = 'CLEAR', command = lambda:self.clear_canvas())
        #self.clear_button.grid(row = 0, column = 0, sticky = 'e')
        #self.plot_button = tk.Button (self.frame_jv, text = 'PLOT', command = lambda:self.plot())
        #self.plot_button.grid(row = 0, column = 0)




    ######################################################################  FUNCTIONS  ###################################################################

    def getDirectory(self,*args):

        """
        Gets the directory path for the exporting of files. 
        Called by the savedir button.
        """

        self.directory = tkinter.filedialog.askdirectory()
        print("Selected directory is: " + str(self.directory))
        self.directory_fill.set(self.directory)

    def directory_fill_setter(self,*args):

        """
        A pointless function merely to fill the box beside the savedir button,
        so that people may confirm that the path they chose is correct.
        (Don't we all doubt the paths we choose)
        """

        self.directory_fill.set(self.directory)


    def showMeasurementType(self, *args):
        """
        A pointless function meant to log the changes to the measurement type, to check
        if the RadioButtons are working. Left here for future debugging.
        """
        mea_type = self.measurement_type.get()
        
        print('Measured Type is = ' + mea_type)

    def showCellType(self, *args):

        """
        A pointless function meant to log the changes to the cell type, to check
        if the RadioButtons are working. Left here for future debugging.
        """

        typecell = self.celltype.get()
        print('Cell type is ' + typecell)

    def selectResource(self,*args):

        """
        Function to select the instrument to use once an option in OptionMenu is clicked.
        """

        rsc = self.selected_resc.get()
        print("Selected resource: " + str(rsc))
        

        # Make connection here
        self.smu = self.rm.open_resource(rsc)
        print("Connection to " + str(rsc) + " successful.")


    def configure_pattern(self,*args):
        
        """
        Function to set the text in the textbox for the pattern scan, because the text in the box is the variable that will be sent
        to the start() function eventually.
        """
        
        collected_pattern = self.scan_dir.get()
        print("Collected pattern is: " + collected_pattern)

        if collected_pattern == 'f':
            pattern = 'f'
            print("Reached 83")
            self.pattern_entry.set('f')
            #pattern_box = Entry (frame_in_par, textvariable = pattern_entry)
            #pattern_box.grid (row = 19, column = 1, sticky = 'w')
            a = 1

        elif collected_pattern == 'r':
            pattern = 'r'
            print("Reached 88")
            self.pattern_entry.set('r')
            #pattern_box = Entry (frame_in_par, textvariable = pattern_entry)
            #pattern_box.grid (row = 19, column = 1, sticky = 'w')
            a = 2
        else:
            self.pattern_entry.set("Enter pattern here.")
            #pattern_box = Entry (frame_in_par, textvariable = pattern_entry)
            #pattern_box.grid (row = 19, column = 1, sticky = 'w')
            a = 3
        
        return a
        

    def showTimeOut(self,*args):

        """
        A pointless function meant to log the changes to the TimeOut box, to check
        if the RadioButtons are working. Left here for future debugging.
        """

        tout = self.timeout.get()
        print('Timeout set to '+str(tout))


    def show_status(self):

        """
        Function to show the connection to the VISA resource.
        """

        Label (self.frame_ic, text = f"Connected to: {self.smu}").grid(row = 1, column = 1)



    def start(self):

        """
        Starts the scanning process. Calls the plot() as well, to plot the data immediately after receiving the data from the Keithley.

        Here, the patterning will be handled instead. The idea is to attempt to plot and export the files with each scan, rather than to do all at once.
        Two functions will be required here.
        1) Running the JV code
            1.1 Running the scan
            1.2 Calculating the parameters
            1.3 Exporting the csv file
        2) Plotting the graph

        Hence, the loop is placed here instead.
        """

        self.clear_canvas()

        print("Pattern is " + str(self.pattern_box.get()))
        
        for i in range(len(str(self.pattern_box.get()))):
            

            save_params = [self.directory_box.get(),\
                            self.op_name_box.get(),\
                            self.sample_id_box.get(),\
                            self.measurement_type.get(),\
                            self.celltype.get(),\
                            self.temp_box.get() \
            ]

            test_output = kvs.sweep_operation(self.smu, \
                                                int(self.steps_no_box.get()), \
                                                self.pattern_box.get(), \
                                                int(self.delay_box.get()), \
                                                float(self.min_volt_box.get()), \
                                                float(self.max_volt_box.get()), \
                                                float(self.scan_rate_box.get()),\
                                                i,\
                                                float(self.cell_area_box.get()),\
                                                float(self.irr_box.get()),\
                                                float(self.curr_lim_box.get()),\
                                                save_params,\
                                                float(self.timeout_box.get())\
            )
            
            # Receive the data and set it as an object variable.
            self.dict_data = test_output

            # This is sent to the plot() function to be the label for that line, and will appear in the legend.
            repetition = "Scan " + str(i+1)

            temp_df = pd.DataFrame.from_dict(self.dict_data)
            
            # Calls the plot function to plot it immediately.
            self.plot(temp_df,self.canvas,repetition)
            
            # This is if the user wants a pause between multiple scans. Default value is set to 0.
            sleep(float(self.multidelay_box.get()))



    def stop(self):
        
        """
        Method to call the stop process from the Keithley scanner py file.
        
        (Does not seem to work. The Keithley only responds to several commands while it is scanning, and in any case,
        this program sleeps while waiting for the data from Keithley, so the program freezes while scanning. Threading likely
        required for such functionality)
        """

        kvs.stop_scan(self.smu)



    def clear_canvas (self):
        
        """
        Function to reset the matplotlib canvas.
        """


        self.graph_container = tk.Canvas (self.frame_jv, height = 400, width = 600, bg = 'white')
        self.graph_container.grid(row = 1, column = 0)
        self.fig = Figure(figsize = (6, 4), dpi = 100)
        self.plot1 = self.fig.add_subplot(111)
        self.plot1.set_xlabel('Voltage (V)')
        self.plot1.set_ylabel('Current Density (mA/cm2)')
        self.plot1.set_yticks([0], minor = True)
        self.plot1.yaxis.grid(True)
        self.plot1.xaxis.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.frame_jv)  
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 1, column = 0)





   


    def plot(self,data,canvas,rep):
    
        # the figure that will contain the plot

        """
        Function to plot the data. This will be called from the start(). That way, a new plot can be made each time the Keithley sends 
        over a set of data from each scan. 
        """

        # Since most of the plotting variables have been declared earlier in the clear.canvas() function, and these variables are object variables,
        # no need to call them here. 
        
        self.plot1.plot(data['Potential (V)'],data['Current Density (mA/cm2)'],linewidth=3,label=rep)
        self.plot1.legend(loc="lower left")

    

        self.fig.canvas.draw()
    
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row = 1, column = 0)

        # This is essential, for ensuring that the plot shows right after data is received. Without this update(), for multiple scans, the plot will
        # only appear after all scans are done. With update(), the canvas is updated with each iteration of the loop in start().

        self.update()
        




if __name__ == "__main__":
    app = Application()  # Create the tk object (the program itself)
    app.mainloop() # Run the mainloop() as required. 

