#!/usr/bin/env python
# coding: utf-8

#  Keithley 2612B SMU TFT Characterization

#  Libraries

from keithley2600 import Keithley2600
import numpy as np
import os
import pyvisa


# Connecting the instrument

rm = pyvisa.ResourceManager()

address = rm.list_resources()

if len(address) == 0:
    print ('No device connected')
    
else:   
    print ('VISA address of the connected devices are:')
    
    for i in range(len(address)):
        print (f"i: {address[i]}")
    
    
    is_valid_input = False 
    
    while(not is_valid_input):
        
        connection_check = input ('Is the VISA address of the SMU listed? (Y/N)')
        
        if connection_check == 'Y' or  connection_check == 'y':
            is_valid_input = True
            smu_index = input('Enter the index number of the SMU:')
            k = Keithley2600(address[smu_index])
            print ('Connected successfully!')

        
        elif connection_check == 'N' or connection_check == 'n': 
            is_valid_input = True 
            print ('Please ensure that the SMU is connected properly')
    
        else: 
            print ('Invalid entry. Please try again.')
        
   








