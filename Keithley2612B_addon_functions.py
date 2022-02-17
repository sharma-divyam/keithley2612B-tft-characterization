import pandas as pd
import datetime
import os
import csv

def oplist_getter():
    
    """
    Function to extract out user data from a text file.

    This function will look for a .txt file in a specific location. The .txt file is meant to contain:

    1) The path for the database which will contain everyone's data.
    2) The list of operators


    This .txt file will be stored in a central location (C:\Windows). This path can be freely changed.

    In the text file, the first line is the path, and the rest of the lines are for operators. They should be separated by the newline character.

    e.g. 

    C:\\Windows\\JV_Scanner --> Path to database
    Person1 --> List of operators
    Person2
    ...

    """

    # Import the new list as a dataframe. \t is used as the delimiter since it is a Notepad txt file.
    # Expected output is a single column

    op_df = pd.read_csv("C:\\Windows\\JV_Scanner\\oplist.txt",sep='\t',engine='python',header=None)

    # Get the relevant data and export as a single list.

    op_list = op_df[0].tolist()

    return op_list


def csv_file_handler(filepath):
    
    
    """
    The Database folder will contain subfolders with the year as the name of the folder. Each folder will then contain a csv file for each month.
    This reduces the size of each csv file. 
    
    E.g. in DatabaseJV folder --> 2020,2021,2022,... and in folder '2020' --> 2020-01.csv, 2020-02.csv, etc...
    
    This function checks if a folder with the current year is already present. If not, it creates one. Then it navigates into that folder to check if
    a csv file for the current month has been created. It creates one if not already created.
    
    The function then returns the handle of the opened csv file.
    
    This function is called from the export_to_database function.
    
    """
    
    current_month = int(datetime.datetime.now().month)
    current_year = int(datetime.datetime.now().year)
    
    
    # Create new folder if not exist. Year name goes into the folder.
    if os.path.isdir(str(current_year)) == False:
        os.mkdir(filepath + "\\" + str(current_year))
        filepath = filepath + "\\" + str(current_year)
    
    else:
        filepath = filepath + "\\" + str(current_year)
    
    
    
    if current_month < 10:
        strmonth = "0" + str(current_month)
    else:
        strmonth = str(current_month)
    
    fullname = filepath + "\\" + str(current_year)+"-"+strmonth+".csv"
    
    # Check if csv file exists
    if os.path.isfile(fullname) == False:
        
        header = ['Operator','Sample_ID','Cell_Type','Measurement_Type','Temp (degC)','Irradiance (Sun(s))','DateCreated','MinVolt (V)','MaxVolt (V)','ScanPattern','LoopNumber',\
            'Voc (V)','Isc (mA)','Jsc (mA/cm2)','Imax (mA)','Vmax (V)','Pmax (mW/cm2)','FF (%)','PCE (%)','Rseries (ohm)','Rshunt (ohm)','CellArea (cm2)','ScanRate (mV/s)','ActualScanRate (mV/s)','HysteresisIndex (%)'\
            'ErrorVoc (V)','ErrorIsc (mA)','ErrorJsc (mA/cm2)','ErrorImax (mA)','ErrorVmax (V)','ErrorPmax (mW/cm2)','ErrorFF (%)','ErrorPCE (%)','ErrorRseries (ohm)','ErrorRshunt (ohm)','ErrorCellArea (cm2)','ErrorScanRate (mV/s)','ErrorActualScanRate (mV/s)','ErrorHysteresisIndex (%)',\
            'Voltages (V)', 'Currents (A)','Timestamps (s)']
        
        # HYSTERESIS INDEX, LOOP NUMBER, SCAN_PATTERN are all included.
        
        # Create new csv file.
        with open(fullname,'a',encoding='UTF8',newline='') as g:
            
            writer = csv.writer(g)
            writer.writerow(header)
        
    else: 
        
        # Open the previous file.
        g = open(fullname,'a',encoding='UTF8',newline='')
    
    
    return g


def export_to_database(metadata,jv_calculated_data,jv_calculated_data_errors,voltages_raw,currents_raw,timestamps_raw,filepath):
    
    handle = csv_file_handler(filepath)
    writer = csv.writer(handle)
    
    # Change raw scan to string values
    
    stringvoltage = str(voltages_raw)
    stringcurrent = str(currents_raw)
    stringtimestamps = str(timestamps_raw)
    
    # Removes the array brackets and commas
    # "[1,2,3,4,5,6,7]" --> "1#2#3#4#5#6#7"
    # No more commas, so it will not be considered as a separate column in the csv format. 
    # This means the entire IV scan, along with the timestamps, can be included into the database file in just three columns.
    # A string.split("#") function can change this to a string list form, which can then be converted back into a float list to be plotted.
    
    stringvoltage = stringvoltage.replace('[','')
    stringvoltage = stringvoltage.replace(']','')
    stringvoltage = stringvoltage.replace(',','#')
    stringcurrent = stringcurrent.replace('[','')
    stringcurrent = stringcurrent.replace(']','')
    stringcurrent = stringcurrent.replace(',','#')
    stringtimestamps = stringtimestamps.replace('[','')
    stringtimestamps = stringtimestamps.replace(']','')
    stringtimestamps = stringtimestamps.replace(',','#')
    
    # Saveparams, jvparams, jvparams_errors are all lists, so just need to append the stringvoltage and the other two; this entire row can then be written to the csv file.
    
    combined = metadata + jv_calculated_data + jv_calculated_data_errors # CHECK DIMENSION IS CORRECT!!!
    combined.extend([stringvoltage,stringcurrent,stringtimestamps])
    
    writer.writerow(combined)
    print("Data saved in database")
    handle.close()
    print("Handle to database closed.")
    
def stop_multiple_scan():
    
    """
    Stops the multiple scans when clicked.
    This does not stop the Keithley from finishing its current run.
    
    This will kill the sweep operation thread, but will wait for the Keithley to finish its scan if it is performing the scan, hence the need for the OPC? querying
    
    """
    pass
    
    