#!/usr/bin/env python

import serial
import time
import rospy
from gcode_sender.msg import Command

s = 0

def openGRBL():
    global s
    s = serial.Serial('/dev/ttyS0', 115200, timeout=0.1) # Open GRBL serial port
    s.write("\r\n\r\n") # Wake up GRBL
    time.sleep(2) # Wait for GRBL to initialize
    rospy.loginfo("***Connected to %s @ %s baud***"%(s.port, s.baudrate))
    grbl_out = s.readline()
    while grbl_out:
        grbl_out = s.readline()

def callback(data):
    global s
    gcode = "G1 X%d Y%d Z%d F100" % (data.x, data.y, data.z) # Create G-code block
    rospy.loginfo("Given command: %s" % gcode) # Log data
    s.write(gcode + '\n')
    grbl_out = s.readline()
    rospy.loginfo(grbl_out.strip())
    s.write("G4P0\n")
    grbl_out = s.readline()
    rospy.loginfo(grbl_out.strip())
    while grbl_out.strip() != "ok":
        grbl_out = s.readline()

def listener():
    rospy.init_node('listener', anonymous = True) # Initialize node
    rospy.Subscriber('position', Command, callback) # Create Subscriber
    rospy.spin() # Wait for shutdown

if __name__ == '__main__':
    try:
        openGRBL()
        listener()
        s.close() # Close serial port
        rospy.loginfo("Shutting down...")
    except serial.SerialException:
        rospy.loginfo("Could not open port /dev/ttyS0. Check serial connection, then try again.")
