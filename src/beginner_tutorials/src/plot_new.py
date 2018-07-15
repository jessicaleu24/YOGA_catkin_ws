#!/usr/bin/env python 
import numpy as np
from matplotlib import pyplot as plt
import rospy
from marvelmind_nav.msg import hedge_pos_a
from nav_msgs.msg import Odometry


gps_state_ = [0,0,0,0]

def plot_(msg):
    global counter
    if counter % 5 == 0:
        gps_state_[0] = msg.timestamp_ms
        gps_state_[1] = msg.x_m
        gps_state_[2] = msg.y_m
        gps_state_[3] = msg.z_m
        
        plt.plot(gps_state_[1], gps_state_[2], 'x')
        plt.axis("equal")
        plt.draw()
        plt.pause(0.00000000001)

    counter += 1

def plot_od(msg_od):
    global counter
    if counter % 20 == 0:
        gps_state_[0] = 0
        gps_state_[1] = msg_od.pose.pose.position.x
        gps_state_[2] = msg_od.pose.pose.position.y
        gps_state_[3] = 0
        
        plt.plot(gps_state_[1], gps_state_[2], '--*')
        plt.axis("equal")
        plt.draw()
        plt.pause(0.00000000001)

    counter += 1

if __name__ == '__main__':
    counter = 0

    rospy.init_node("plot_position")
    rospy.Subscriber("hedge_pos_a", hedge_pos_a, plot_)
    #rospy.Subscriber("/odom", Odometry, plot_od)
    plt.ion()
    plt.show()
    rospy.spin()
