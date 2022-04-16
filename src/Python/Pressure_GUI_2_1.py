# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 20:08:29 2021

@author: Brandon Staton
"""

from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst
import serial
import time
import UAHWindtunnel1 as WT
import os
global pressure_data
import pandas as pd
def connect():
    ConnectionData = WT.connect()
    ArduinoPort = ConnectionData[1]
    ACP = 'Arduino COM Port: ' + ArduinoPort
    ABR = 'BAUD Rate: 115200'
    COM_label.config(text = ACP)
    BAUD_label.config(text = ABR)

def GetPrelim():
    CurrTemp = WT.temp(1)
    CurrTemp = CurrTemp[0]
    CurrTemp = str(CurrTemp)
    TempValue.config(text = 'Temperature: '+CurrTemp + ' C')
    CurrHum = WT.hmd(1)
    CurrHum = CurrHum[0]
    CurrHum = str(CurrHum)
    HumValue.config(text = 'Humidity: '+CurrHum + ' %')
    
def ArCOM():
    ConnectionData = WT.connect()
    ArduinoPort = ConnectionData[1]
    ACP = 'Arduino COM Port: ' + ArduinoPort
    return(ACP)

def ArTemp():
    CurrTemp = WT.temp(1)
    CurrTemp = CurrTemp[0]
    CurrTemp = str(CurrTemp)
    tempVal = 'Temperature: ' + CurrTemp
    return(tempVal)    

def ArHum():
    CurrHum = WT.hmd(1)
    CurrHum = CurrHum[0]
    CurrHum = str(CurrHum)
    ACP = 'Humidity: ' + CurrHum
    return(ACP)

xlim = 140
ylim = 140

global curr_x
global curr_y
curr_x = 0
curr_y = 0

root = Tk()
root.title('Pitot Pressure')

# Setup Section----------------------------------------------------------------
SetupFrame = LabelFrame(root, text = 'Setup', padx = 5, pady = 5)
SetupFrame.grid(row = 1, column = 0, padx = 10, pady=5)

COM_label = Label(SetupFrame,text = 'Arduino COM Port:  TBD')
COM_label.grid(row = 0, column = 0)
BAUD_label = Label(SetupFrame, text = 'BAUD Rate:    TBD')
BAUD_label.grid(row = 1, column = 0)

SetupButton = Button(SetupFrame,text='Connect to Arduino',command = connect)
SetupButton.grid(row = 2, column =0)



# Current Temp Section-----------------------------------------------------
Prelim = LabelFrame(root, text = 'Preliminary Info',padx=5,pady=5)
Prelim.grid(row=1, column = 1, padx = 10, pady = 5)

TempValue = Label(Prelim,text = 'Temperature:  TBD')
TempValue.grid(row = 0, column = 0)

HumValue = Label(Prelim,text = 'Humidity:  TBD')
HumValue.grid(row = 1, column = 0)

GetTempButton = Button(Prelim,text='Get Current Temp and Humidity',command = GetPrelim)
GetTempButton.grid(row = 2, column = 0)


#------------------------------------------------------------------------------
# File Info
File_info_frame = LabelFrame(root, text = 'File Information', padx = 8,
                             pady = 5)
File_info_frame.grid(row = 0, column = 0, columnspan=2, padx = 10, pady = 10)

# error handling for file path
def browse_directory():
    global filename
    filename = filedialog.askdirectory()
    if str(filename) != '':
        file_directory.config(state = NORMAL)
        file_directory.delete(0,END)
        file_directory.insert(END, str(filename))
        file_directory.config(state = DISABLED)
        def_file_path_popup()

# checks if the default file directory is valid
def default_file_directory():
    GD = open('GUI_Defaults.txt', 'r')
    user_def_dir = GD.read()
    GD.close()
    if os.path.exists(user_def_dir) == False:
        user_def_dir = os.getcwd()
        GD = open('GUI_Defaults.txt', 'w')
        GD.write(user_def_dir)
        GD.close()
        

file_path_text = Label(File_info_frame, text = 'Directory of File Output: ')
file_path_text.grid(column = 0, row = 0)

default_file_directory()
GD = open('GUI_Defaults.txt', 'r')
folder_path = GD.read()
GD.close()

file_directory = Entry(File_info_frame)
file_directory.insert(END, str(folder_path))
file_directory.config(state = DISABLED)
file_directory.grid(column = 0, row = 0, ipadx = 100, columnspan = 3)
file_browse_button = Button(File_info_frame, text = 'Browse', 
                            command = browse_directory)
file_browse_button.grid(column = 4, row = 1, padx = 5)

spacer_text = Label(File_info_frame, text = ' ')
spacer_text.grid(row = 2, column = 0)

data_file_name_text = Label(File_info_frame, text = 'Data File Name: ')
data_file_name_text.grid(column = 0, row = 3)
data_file_name = Entry(File_info_frame)
data_file_name.grid(row = 3, column = 1)


# Data Acquisition ----------------------------------------------------------
DA = LabelFrame(root, text = 'Data Acquisition', padx = 5, pady = 5)
DA.grid(row = 2, column = 1, padx = 10, pady = 5)
integration_time_text = Label(DA, text = 'Time Between Readings: ')
integration_time_text.grid(row = 2, column = 0)
integration_time_box = Spinbox(DA, from_= 1, to = 99999, width = 5)
integration_time_box.grid(column = 1, row = 2, pady = 3)
integration_time_units = Label(DA, text = ' miliseconds')
integration_time_units.grid(column = 2, row = 2)

dataPoints_time_text = Label(DA, text = 'Data Points: ')
dataPoints_time_text.grid(row = 3, column = 0)
dataPoints_time_box = Spinbox(DA, from_= 1, to = 99999, width = 5)
dataPoints_time_box.grid(column = 1, row = 3, pady = 3)
dataPoints_time_units = Label(DA, text = ' Reading(s)')
dataPoints_time_units.grid(column = 2, row = 3)

# Pitot Movement ----------------------------------------------------------
PM = LabelFrame(root, text = 'Pitot Movement', padx = 5, pady = 5)
PM.grid(row = 2, column = 0, padx = 10, pady = 5)
x_loc_text = Label(PM,text = 'x-Location: ')
x_loc_text.grid(row = 0, column = 0)
x_loc_spinbox = Spinbox(PM,from_=0, to = xlim, width = 5)
x_loc_spinbox.grid(row = 0, column = 1)
x_loc_units = Label(PM, text = ' millimeters')
x_loc_units.grid(row = 0, column = 2)

y_loc_text = Label(PM,text = 'y-Location: ')
y_loc_text.grid(row = 1, column = 0)
y_loc_spinbox = Spinbox(PM,from_=0, to = ylim, width = 5)
y_loc_spinbox.grid(row = 1, column = 1)
y_loc_units = Label(PM, text = ' millimeters')
y_loc_units.grid(row = 1, column = 2)

def pitotMoveCmd():
    global curr_x
    global curr_y
    new_x_loc = x_loc_spinbox.get()
    new_x_loc = int(new_x_loc)
    new_y_loc = y_loc_spinbox.get()
    new_y_loc = int(new_y_loc)
    if new_x_loc > xlim:
       x_loc_spinbox.delete(0,'end')
       x_loc_spinbox.insert(0,str(xlim))
    elif new_x_loc < 0:
       x_loc_spinbox.delete(0,'end')
       x_loc_spinbox.insert(0,str(0))
    elif new_y_loc > ylim:
       y_loc_spinbox.delete(0,'end')
       y_loc_spinbox.insert(0,str(ylim))      
    elif new_y_loc < 0:
       y_loc_spinbox.delete(0,'end')
       y_loc_spinbox.insert(0,str(0)) 
    else:
        print('Current y loc: ' + str(curr_y))
        x_move_dst = new_x_loc - curr_x
        y_move_dst = new_y_loc - curr_y
        print('Distance to move: ' + str(y_move_dst))
        if x_move_dst < 0:
            WT.move_xpositive(x_move_dst/10)
        if x_move_dst > 0:
            WT.move_xnegative(abs(x_move_dst/10))
        if y_move_dst > 0:
            WT.move_ypositive(y_move_dst/10)
        if y_move_dst < 0:
            WT.move_ynegative(abs(y_move_dst/10))
        curr_x = new_x_loc
        curr_y = new_y_loc
        print('Current y location: ' + str(curr_y))

goto_button = Button(PM,text = 'Goto Location', command = pitotMoveCmd)
goto_button.grid(row = 2, column = 2)





# Confirmation Section---------------------------------------------------------
def confirmClick():
    timeBetweenReadings = int(integration_time_box.get())
    totalDataPoints = int(dataPoints_time_box.get())
    filepathSansFileName = file_directory.get()
    txtFile = data_file_name.get()
    totalFilePath = filepathSansFileName + "\\" + txtFile + ".xlsx"
    if os.path.exists(totalFilePath):
        print('Path Exists')
        local_time = time.ctime(time.time())    
        txtDataFile = open(totalFilePath,"w+")
        pressure_data = WT.pressure(totalDataPoints,timeBetweenReadings)
        print(pressure_data)
        df = pd.DataFrame(pressure_data, columns = ['Pressure [pa]'])
        df.to_excel(totalFilePath, index = False)
        
    else:
        print('Path Doesnt Exist')
        pressure_data = WT.pressure(totalDataPoints,timeBetweenReadings)
        print(pressure_data)
        df = pd.DataFrame(pressure_data, columns = ['Pressure [pa]'])
        df.to_excel(totalFilePath, index = False)
        
def exitClick():
    global curr_x
    global curr_y
    WT.move_xnegative(curr_x)
    WT.move_ynegative(curr_y)
    root.destroy()
    
DS = LabelFrame(root, text = 'Confirmation', padx = 5, pady = 5)
DS.grid(row=3,column = 1, padx = 10, pady=5)

Start = Button(DS,text='Start Data Acquisition',command = confirmClick)
Start.grid(row = 0, column = 0, padx = 5)

Exit = Button(DS,text='Exit',command = exitClick)
Exit.grid(row = 0, column = 1, padx = 5)




root.mainloop()