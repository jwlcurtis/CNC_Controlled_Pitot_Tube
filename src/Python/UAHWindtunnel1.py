# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:27:40 2021

@author: logan
"""
import warnings
import serial
import serial.tools.list_ports
import time
import numpy as np
import pandas as pd

global ser
def connect():
    """
    Automatically opens a serial connection to arduino
    at 11520. Connectes to First arduino if multiple are found.
    """
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description  # may need tweaking to match new arduinos
        ]
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        warnings.warn('Multiple Arduinos found - using the first')

    ser = serial.Serial(arduino_ports[0], baudrate=115200, timeout=5)
    ser.close()
    ser.open()
    ConnectionInfo = arduino_ports[0]
    time.sleep(2)
    return(ser,ConnectionInfo)
    
def disconnect(ser):
    """
    Closes Arduino Serial connection
    """
    ser.close()
    
def temp(i):
    """
    Commands the arduino to take i amount of temperture measurements
    and returns the values in the veriable tempdata in celsius
    """
    ser,Hm=connect()
    ser.write(bytes("temp",'utf-8'))
    time.sleep(0.75)
    ser.write(str.encode(str(i)))
    tempdata=np.zeros(i, dtype=float)
    for x in range(i):
        time.sleep(1)
        s = ser.readline()
        tempdata[x]=float(s)
    disconnect(ser)
    return(tempdata)

def hmd(i):
    """
    Commands the arduino to take i amount of Humidity measurements
    and returns the values in the veriable hmddata in %
    """
    ser,Hm=connect()
    ser.write(bytes("hmd",'utf-8'))
    time.sleep(0.75)
    ser.write(str.encode(str(i)))
    hmddata=np.zeros(i, dtype=float)
    for x in range(i):
        time.sleep(1)
        s = ser.readline()
        hmddata[x]=float(s)
    disconnect(ser)
    return(hmddata)

def home_x():
    """
    Homes the x axis of CNC control
    """
    ser,Hm=connect()
    ser.write(bytes("homex",'utf-8'))
    time.sleep(0.75)
    disconnect(ser)
def home_y():
    """
    Homes the x axis of CNC control
    """
    ser,Hm=connect()
    ser.write(bytes("homey",'utf-8'))
    disconnect(ser)

def move_xpositive(distance):
    """
    moves X-axis by distance [cm] in the positive direction
    """ 
    ser,Hm=connect()
    ser.write(bytes("xpositive",'utf-8'))
    time.sleep(0.75)
    ser.write(str.encode(str(distance)))
    disconnect(ser)
def move_ypositive(distance):
    """
    moves Y-axis by distance [cm] in the positive direction
    """ 
    ser,Hm=connect()
    ser.write(bytes("ypositive",'utf-8'))
    time.sleep(0.75)
    ser.write(str.encode(str(distance)))
    disconnect(ser)
def move_ynegative(distance):
    """
    moves Y-axis by distance [cm] in the negative direction
    """ 
    ser,Hm=connect()
    ser.write(bytes("ynegative",'utf-8'))
    time.sleep(0.75)
    ser.write(str.encode(str(distance)))
    disconnect(ser)
def move_xnegative(distance):
    """
    moves X-axis by distance [cm] in the negative direction
    """ 
    ser,Hm=connect()
    ser.write(bytes("xnegative",'utf-8'))
    time.sleep(0.75)
    ser.write(str.encode(str(distance)))
    disconnect(ser)
    
def pressure(readings,delay):
    """
    reading pressure values
    """ 
    ser,Hm=connect()
    ser.write(bytes("pressure",'utf-8'))
    time.sleep(0.75)
    ser.write(str.encode(str(readings)))
    time.sleep(0.75)
    ser.write(str.encode(str(delay)))
    pressuredata=np.zeros(readings, dtype=float)
    for x in range(readings):
        #time.sleep(1)
        s = ser.readline()
        pressuredata[x]=float(s)
    disconnect(ser)
    return(pressuredata)
def save(file):
    df = pd.DataFrame(pressure_data, columns = ['Pressure [pa]'])
    df.to_excel(file, index = False)
    print(df)