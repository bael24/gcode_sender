#!/usr/bin/env python

import serial
import time
import pdb

s = 0

def openGRBL():
    global s
    s = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1) # Open GRBL serial port
    s.write("\r\n\r\n") # Wake up GRBL
    time.sleep(2) # Wait for GRBL to initialize
    #s.flushInput() # Flush startup text in serial input
    #pdb.set_trace()
    print("***Connected to %s @ %s baud***"%(s.port, s.baudrate))
    grbl_out = s.readline()
    while grbl_out:
        print(grbl_out.strip())
        grbl_out = s.readline()

def interfaceGRBL():
    global s
    while True:
        try:
            msg = raw_input(">>> ")
            s.write(msg + '\n')
            grbl_out = s.readline()
            while grbl_out.strip():
                print(grbl_out.strip())
                grbl_out = s.readline()
        except KeyboardInterrupt:
            print("Terminated")
            break

if __name__ == '__main__':
    try:
        openGRBL()
        interfaceGRBL()
        s.close() # Close serial port
        print("Shutting down...")
    except serial.SerialException:
        print("Could not open port /dev/ttyUSB0. Check serial connection, then try again.")


