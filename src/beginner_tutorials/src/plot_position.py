#!/usr/bin/env python 
import numpy as np
from matplotlib import pyplot as plt
import rospy
from marvelmind_nav.msg import hedge_pos_a

gps_state_ = [0,0,0,0]

def plot_(msg):
    global counter
    if counter % 20 == 0:
        gps_state_[0] = msg.timestamp_ms
        gps_state_[1] = msg.x_m
        gps_state_[2] = msg.y_m
        gps_state_[3] = msg.z_m
        
        plt.plot(gps_state_[1], gps_state_[2], '--*')
        plt.axis("equal")
        plt.draw()
        plt.pause(0.00000000001)

    counter += 1

if __name__ == '__main__':
    counter = 0

    rospy.init_node("plot_position")
    rospy.Subscriber("hedge_pos_a", hedge_pos_a, plot_)
    plt.ion()
    plt.show()
    rospy.spin()
