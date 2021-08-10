#!/usr/bin/env python
# coding: utf-8

#  Keithley 2612B SMU TFT Characterization

#  Libraries

from keithley2600 import Keithley2600
import numpy as np
import pyvisa
import csv
from datetime import datetime


def get_target_volt(start_volt):
    """
    Return the target volt. Check validity of the input.

    :param start_volt: The starting point of the voltage sweep. 

    """
    while True:
        # Keeps asking the user for the valid target volt until they correclty provide one.
        target_volt = float (input ('Set the target voltage (in Volts) for sweep: '))
        
        if target_volt > start_volt:
            return target_volt
        else: 
            print ('INVALID INPUT: Target voltage must be greater than starting voltage.')

def get_step_volt(start_volt, target_volt):
    """
    Return the step volt. It is the magnitude of steps in which the sweep will occur. Check validity of the input.

    :param start_volt: The starting point of the voltage sweep. 
    :param target_volt: The end point of the voltage sweep. 

    """
    while True:

        step_volt = float (input ('Set the size of steps (in Volts) of sweep: ')) 
        
        if step_volt <= target_volt - start_volt:
            return step_volt
        else:
            print ('INVALID INPUT: Step must be less than or equal to the difference between starting and target voltage')

def get_integration_time ():
    """
    Return integration time. Check if input is within the range suggested by Keithley2600 manual.

    """
    while True:
        integration_time = float (input('Set the integration time for each data point (in PLC): '))
        if integration_time >= 0.001 and integration_time <= 25:
            return integration_time
        else: 
            print('INVALID INPUT: The integration time must be between 0.001 and 25 PLC.')

def get_sweep_type():
    """
    Return boolean for sweep type based on the character input.
    """
    while True:
        sweep_type = input ('Choose between pulsed and continuous sweep (enter P or C): ')
        if sweep_type == 'P' or sweep_type == 'p':
            return True  
        elif sweep_type == 'C' or sweep_type == 'c':
            return False
        else:
            print ('INVALID INPUT')

def sweep_operation(smu_id, steps_no, measure_delay, nplc, start, end):

    v_measured, i_measured, timestamps = [], [], []
    
    smu_id.trigger.count = steps_no

    smu_id.measure.delay = measure_delay
    smu_id.measure.nplc = nplc
    
    smu_id.source.func = smu_id.OUTPUT_DCVOLTS

    smu_id.nvbuffer1.clear()
    smu_id.nvbuffer2.clear()
    smu_id.nvbuffer1.clearcache()
    smu_id.nvbuffer2.clearcache()

    smu_id.nvbuffer2.collecttimestamps = 1

    smu_id.trigger.measure.iv(smu_id.nvbuffer1, smu_id.nvbuffer2)

    smu_id.trigger.source.linearv (start, end, steps_no)

    smu_id.trigger.source.action = smu.ENABLE
    smu.trigger.measure.action = smu.ENABLE

    smu_id.source.output = smu_id.OUTPUT_ON
    smu_id.trigger.initiate()

    v_measured = smu_id.nvbuffer2.readings
    i_measured = smu_id.nvbuffer1.readings
    timestamps = smu_id.nvbuffer2.timestamps

    output = [v_measured, i_measured, timestamps]

    smu_id.nvbuffer1.clear()
    smu_id.nvbuffer2.clear()
    smu_id.nvbuffer1.clearcache()
    smu_id.nvbuffer2.clearcache()

    return output
    """
    output index -> stored parameter
    0 -> voltage in Volt 
    1 -> current in Ampere
    2 -> timestamps (not sure of the format)
    
    """


# Connecting the instrument

rm = pyvisa.ResourceManager()
address = rm.list_resources()

if len(address) == 0:
    print ('No device connected')
    
else:
    print ('VISA address of the connected devices are:')
    
    for i in range(len(address)):
        print (f"{i}: {address[i]}")
    
    
    is_valid_input = False
    
    while not is_valid_input:

        get_address_existence = input ('Is the VISA address of the SMU listed? (Y/N): ').lower()

        if get_address_existence == 'y':
            is_valid_input = True
            smu_index = int(input('Enter the index number of the SMU: '))
            k = Keithley2600(address[smu_index])
            smu = rm.open_resource(address[smu_index])
            is_connected = True
            print ('Connected successfully!', '/n')

            print ('VOLTAGE SWEEP PARAMETERS:', '/n')

            # Voltage sweep parameters

            # Source voltage from Channel A

            start_volt = float (input ('Set the starting voltage (in Volts) for sweep: '))

            target_volt = get_target_volt(start_volt)
            
            steps_num = int (input ('Enter the number of steps'))
            """
            step_volt = get_step_volt(start_volt, target_volt)

            if (target_volt - start_volt) % step_volt == 0:
                sweep_volt = np.arange (start_volt, target_volt + step_volt, step_volt)
            else:
                sweep_volt = np.arange (start_volt, target_volt, step_volt)
            """
            integration_time = get_integration_time()
            

            measure_delay = float (input('Set settling delay (in seconds) before each measurement: (NOTE: Setting the value to -1 automatically starts taking measurement as soon as current is stable) '))

            #pulsed = get_sweep_type()

            
            # VI measurement
            print ('Voltage sweep being conducted...')
            test_output = sweep_operation (smu, steps_num, measure_delay, integration_time, start_volt, target_volt) 
            end_time = datetime.now()
            print (f"Sweep successfully completed on {end_time}.")

            # scan rate 
            # (Unsure of the data type of measured voltage and timestamps. This will only work if both are float or int)   
    
            del_t = []
            for i in len(test_output[2]):
                del_t [i] = test_output [2][i] - test_output [2][0]

            scan_rate = np.polyfit(del_t, test_output[0], 1)[0]

            print (f"The scan rate of the sweep operation was {scan_rate} V/s")

              

            # Data acquisition
            vi_output = [test_output[0], test_output[1]]
            title = str (input('Give a title for the test conducted: '))
            vi_output_transpose = np.transpose(vi_output)
            file_path = str (input('Give file path and file name (with .csv extension) to record the data: '))
            headers = ['Voltage (in Volt)', 'Current (in Ampere)', 'Timestamp']

            with open(file_path, 'w+') as csv_file:
                write = csv.writer(csv_file)
                write.writerow(title)
                write.writerow(headers)
                write.writerows(vi_output_transpose)
                write.writerow(f"Date and Time of measurement: {end_time }")

        
        elif get_address_existence == 'n': 
            is_valid_input = True
            print ('Please ensure that the SMU is connected properly')


        else: 
            print ('INVALID INPUT')

        

