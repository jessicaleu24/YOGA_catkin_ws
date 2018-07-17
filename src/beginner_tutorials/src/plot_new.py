#!/usr/bin/env python 
import numpy as np
from matplotlib import pyplot as plt
import rospy
from marvelmind_nav.msg import hedge_pos_a
from nav_msgs.msg import Odometry


gps_state_ = [0,0,0,0]
od_state_ = [0,0,0]

def calibrate():
    global offset_store 
    global counter
    global offset
    offset_store = np.zeros((2,20))
    offset = np.zeros((2,1))

    while counter<20:
    	rospy.Subscriber("hedge_pos_a", hedge_pos_a, plot_)
        offset_store[0][counter] = gps_state_[1]
        offset_store[1][counter] = gps_state_[2] 
        
        counter += 1
    offset = np.mean(offset_store,axis=1)
    
    

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
        od_state_[0] = 0
        od_state_[1] = msg_od.pose.pose.position.x
        od_state_[2] = msg_od.pose.pose.position.y
       
        
        plt.plot(od_state_[1], od_state_[2], '--*')
        plt.axis("equal")
        plt.draw()
        plt.pause(0.00000000001)

    counter += 1

if __name__ == '__main__':
    counter = 0
    #calibrate()
    rospy.loginfo('Calibration done!! Let\'s go!')

    rospy.init_node("plot_position")
    rospy.Subscriber("hedge_pos_a", hedge_pos_a, plot_)
    rospy.Subscriber("/odom", Odometry, plot_od)
    plt.ion()
    plt.show()
    rospy.spin()
