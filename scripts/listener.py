#!/usr/bin/env python

import rospy
import serial
import time
from gcode_sender.msg import Command
from sensor_msgs.msg import Joy

s = 0

def callback(data):
    global s
    gcode = "G0 X%d Y%d Z%d" % (data.x, data.y, data.z) # Create G-code block
    rospy.loginfo("Given command: %s" % gcode) # Log data
    s.write(gcode + '\n') # Send g code block to grbl
    grbl_out = s.readline() # Wait for GRBL response with carriage return
    print("Response: " + grbl_out.strip()) # Print response without EOL characters

def callbackJoy(data):
    global s
    positionX = data.axes[1]/5
    positionY = data.axes[0]/5
    positionZ = data.axes[4]/5
    if positionX == 0 and positionY == 0 and positionZ == 0:
        gcode = chr(133)
    else:
        gcode = "$J=G91 X%s Y%s Z%s F100" % (positionX, positionY, positionZ) # Create G-code block
    rospy.loginfo("Given command: %s" % gcode) # Log data
    s.write(gcode + '\n') # Send g code block to grbl
    grbl_out = s.readline() # Wait for GRBL response with carriage return
    print("Response: " + grbl_out.strip()) # Print response without EOL characters

def listener():
    rospy.init_node('listener', anonymous = True) # Initialize node
    rospy.Subscriber('position', Command, callback) # Create Subscriber
    rospy.Subscriber('joy', Joy, callbackJoy) # Create Joystick subscriber
    rospy.spin() # Wait for shutdown

def openGRBL():
    global s
    s = serial.Serial('/dev/ttyUSB0', 115200) # Open GRBL serial port
    s.write("\r\n\r\n") # Wake up GRBL
    time.sleep(2) # Wait for GRBL to initialize
    s.flushInput() # Flush startup text in serial input

if __name__ == '__main__':
    openGRBL()
    listener()
    s.close() # Close serial port
    rospy.signal_shutdown("Terminated by Ctrl+C")
    print("Shutting down")


