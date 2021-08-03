#!/usr/bin/env python
# coding: utf-8

#  Keithley 2612B SMU TFT Characterization

#  Libraries

from keithley2600 import Keithley2600
import numpy as np
import pyvisa
import csv


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
            is_connected = True
            print ('Connected successfully!', '/n')

            print ('VOLTAGE SWEEP PARAMETERS:', '/n')

            # Voltage sweep parameters

            # Source voltage from Channel A

            start_volt = float (input ('Set the starting voltage (in Volts) for sweep: '))

            target_volt = get_target_volt(start_volt)
            
            step_volt = get_step_volt(start_volt, target_volt)

            if (target_volt - start_volt) % step_volt == 0:
                sweep_volt = np.arange (start_volt, target_volt + step_volt, step_volt)
            else:
                sweep_volt = np.arange (start_volt, target_volt, step_volt)
            
            integration_time = get_integration_time()

            delay_time = float (input('Set settling delay (in seconds) before each measurement: (NOTE: Setting the value to -1 automatically starts taking measurement as soon as current in stable) '))

            pulsed = get_sweep_type()

            # VI measurement
            vi_output = k.voltage_sweep_single_smu (k.smua, sweep_volt, integration_time, delay_time, pulsed)

            # Data acquisition
            vi_output_transpose = np.transpose(vi_output)
            file_path = str (input('Give file path and file name (with .csv extension) to record the data: '))
            headers = ['Voltage (in Volt)', 'Current (in Ampere)']

            with open(file_path, 'w+') as csv_file:
                write = csv.writer(csv_file)
                write.writerow(headers)
                write.writerows(vi_output_transpose)

        
        elif get_address_existence == 'n': 
            is_valid_input = True
            print ('Please ensure that the SMU is connected properly')


        else: 
            print ('INVALID INPUT')

        

