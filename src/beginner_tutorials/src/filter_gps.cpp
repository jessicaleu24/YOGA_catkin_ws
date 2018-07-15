

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "marvelmind_nav/hedge_pos_a.h"

#include <sstream>

/**
 * This tutorial demonstrates simple receipt of messages over the ROS system.
 */
double gps_state_[4] = {0,0,0,0}; // timestamp, X, Y, Z
double Pre_gps_state_[4] = {0,0,0,0}; // timestamp, X, Y, Z
double filteredGPS_[4] = {0,0,0,0}; // timestamp, X, Y, Z
marvelmind_nav::hedge_pos_a new_msg;
double time_ = 0; 
double Ts = 0; 
double time_new_ =0;



void chatterCallback(const marvelmind_nav::hedge_pos_a &msg)
{
  // Save past information
  time_ = time_new_;
  time_new_ =ros::Time::now().toSec();
  Ts = time_new_-time_;
  Pre_gps_state_[0] = gps_state_[0];
  Pre_gps_state_[1] = gps_state_[1]; 
  Pre_gps_state_[2] = gps_state_[2];
  Pre_gps_state_[3] = gps_state_[3];


  // Get new information
  gps_state_[0] = msg.timestamp_ms;
  gps_state_[1] = msg.x_m; 
  gps_state_[2] = msg.y_m;
  gps_state_[3] = msg.z_m;

  filteredGPS_[2] = gps_state_[2];
  
  // Assign result to publishing message
  new_msg.address= 0;
  new_msg.timestamp_ms = gps_state_[0];
  new_msg.x_m = filteredGPS_[1];
  new_msg.y_m = filteredGPS_[2];
  new_msg.z_m = filteredGPS_[3];
  new_msg.flags = (1<<0);// 'data not available' flag
  


 
  ROS_INFO("I heard: [%f] and [%f] in [%f]", Pre_gps_state_[0],gps_state_[0], Ts);
}

int main(int argc, char **argv)
{
  /**
   * The ros::init() function needs to see argc and argv so that it can perform
   * any ROS arguments and name remapping that were provided at the command line.
   * For programmatic remappings you can use a different version of init() which takes
   * remappings directly, but for most command-line programs, passing argc and argv is
   * the easiest way to do it.  The third argument to init() is the name of the node.
   *
   * You must call one of the versions of ros::init() before using any other
   * part of the ROS system.
   */
  ros::init(argc, argv, "filter_gps");

  /**
   * NodeHandle is the main access point to communications with the ROS system.
   * The first NodeHandle constructed will fully initialize this node, and the last
   * NodeHandle destructed will close down the node.
   */
  ros::NodeHandle n;
  
  ros::Subscriber sub = n.subscribe("/hedge_pos_a", 1000, chatterCallback);
  ros::Publisher filteredGPS_pub = n.advertise<marvelmind_nav::hedge_pos_a>("filteredGPS", 1000);
  ros::Rate loop_rate(2);
  
  // Keep on subscribing and publishing 
   while (ros::ok())
  {
    
    filteredGPS_pub.publish(new_msg);
    ros::spinOnce();    
    loop_rate.sleep();
    
  }


  return 0;
}


