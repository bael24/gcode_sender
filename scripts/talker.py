#!/usr/bin/env python

import rospy
from gcode_sender.msg import Command

def talker():
    pub = rospy.Publisher('position', Command, queue_size = 10)
    rospy.init_node('talker', anonymous = True, disable_signals = True)
    #rate = rospy.Rate(1) # 1 Hz
    msg = Command()

    while not rospy.is_shutdown():
        try:
            print("Please enter the coordinates:")
            msg.x = int(raw_input("X: "))
            msg.y = int(raw_input("Y: "))
            msg.z = int(raw_input("Z: "))

            rospy.loginfo("Command: X=%d, Y=%d, Z=%d" % (msg.x, msg.y, msg.z))
            pub.publish(msg)
            #rate.sleep()
        except KeyboardInterrupt:
            print("Terminating")
            break

if __name__ == '__main__':
    try:
        talker()
        rospy.signal_shutdown("Terminated by Ctrl-C")
        print("Shutdown")
    except rospy.ROSInterruptException:
        pass
