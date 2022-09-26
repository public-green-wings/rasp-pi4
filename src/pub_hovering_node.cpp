#include <ros/ros.h>
#include <std_msgs/String.h> 
#include <stdio.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/SetMode.h>
#include <mavros_msgs/State.h>
#include <mavros_msgs/GlobalPositionTarget.h>
#include <mavros_msgs/PositionTarget.h>
#include <geographic_msgs/GeoPoseStamped.h>
#include "geometry_msgs/PoseStamped.h"
#include "geometry_msgs/Vector3Stamped.h"
#include <sensor_msgs/NavSatFix.h>

//publisher
geographic_msgs::GeoPoseStamped target_pose; //GPS
sensor_msgs::NavSatFix current_pose; //current GPS

//subscriber
mavros_msgs::State current_state;

//Just for arming
void state_cb(const mavros_msgs::State::ConstPtr msg){
    current_state = *msg;
}

//Receive target GPS
void target_cb(const geographic_msgs::GeoPoseStamped msg){
    target_pose = msg;
    //alt_pose.pose.position.altitude = msg.altitude;
    //ROS_INFO("Received(lat,long,alt): %4.2f, %4.2f, %4.2f\n",msg.latitude, msg.longitude, msg.altitude);
}

//Recevie current GPS
void global_cb(const sensor_msgs::NavSatFix msg ){
	current_pose = msg;
	ROS_INFO("Current(lat,long,alt): %4.2f, %4.2f, %4.2f\n",msg.latitude, msg.longitude, msg.altitude);
}

int main(int argc, char **argv)
{
   ros::init(argc, argv, "pub_setpoints");
   ros::NodeHandle n;

	//publishers
   //ros::Publisher move_pub = n.advertise<mavros_msgs::GlobalPositionTarget>("mavros/setpoint_raw/global",10);
   ros::Publisher move_pub = n.advertise <geographic_msgs::GeoPoseStamped> ("mavros/setpoint_position/global", 10); 
   //ros::Publisher rotate_pub = n.advertise <mavros_msgs::PositionTarget> ("mavros/setpoint_raw/local", 10);
   
   //subscribers
   //ros::Subscriber target_sub = n.subscribe<geographic_msgs::GeoPoseStamped>("targeting",10,target_cb); //Realed to SERVER
   ros::Subscriber state_sub = n.subscribe<mavros_msgs::State>("mavros/state", 10, state_cb);
   ros::Subscriber global_sub = n.subscribe<sensor_msgs::NavSatFix>("mavros/global_position/global", 10, global_cb);     
    
   //servicesClient
   ros::ServiceClient arming_client = n.serviceClient<mavros_msgs::CommandBool>("mavros/cmd/arming");
   ros::ServiceClient set_mode_client = n.serviceClient<mavros_msgs::SetMode>("mavros/set_mode");
   
   ros::Rate rate(20.0);
   
    while(ros::ok() && !current_state.connected){
        ros::spinOnce();
        rate.sleep();
    }
    
	target_pose.pose.position.latitude = current_pose.latitude;
    target_pose.pose.position.longitude = current_pose.longitude;
    target_pose.pose.position.altitude = current_pose.altitude-20;
	
	//rotate_pose.yaw = 0;
	//rotate_pose.yaw_rate = 1;
	
	
	//target_pose.latitude = current_pose.latitude;
    //target_pose.longitude = current_pose.longitude;
    //target_pose.altitude = current_pose.altitude + 5;
    
    //alt_pose.pose.position.altitude = current_pose.altitude + 5;
	
    
    //send a few setpoints before starting
    for(int i = 100; ros::ok() && i > 0; --i){
        move_pub.publish(target_pose);
        //alt_pub.publish(alt_pose);
        ros::spinOnce();
        rate.sleep();
    }

    mavros_msgs::SetMode offb_set_mode;
    offb_set_mode.request.custom_mode = "OFFBOARD";
	
    mavros_msgs::CommandBool arm_cmd;
    arm_cmd.request.value = true;

   ros::Time last_request = ros::Time::now();
	float count=0;
   while(ros::ok()){
       target_pose.header.stamp = ros::Time::now();
       //rotate_pose.header.stamp = ros::Time::now();
       target_pose.header.frame_id = 1;
       //rotate_pose.header.frame_id = 1;
       
       if( current_state.mode != "OFFBOARD" &&
            (ros::Time::now() - last_request > ros::Duration(5.0))){
            if( set_mode_client.call(offb_set_mode) &&
                offb_set_mode.response.mode_sent){
                ROS_INFO("Offboard enabled");
            }
            last_request = ros::Time::now();
            
             for(int i = 100; ros::ok() && i > 0; --i){
				move_pub.publish(target_pose);
				//alt_pub.publish(alt_pose);
			}
        } else if( !current_state.armed &&
                (ros::Time::now() - last_request > ros::Duration(5.0))){
                if( arming_client.call(arm_cmd) &&
                    arm_cmd.response.success){
                    ROS_INFO("Vehicle armed");
                }
                last_request = ros::Time::now();
                 for(int i = 100; ros::ok() && i > 0; --i){
					move_pub.publish(target_pose);
					//alt_pub.publish(alt_pose);
				}
            }
		else{
		
		   move_pub.publish(target_pose);
		   //rotate_pub.publish(rotate_pose);
			//alt_pub.publish(alt_pose);
        }
        
	   //count+=0.01;
	   //rotate_pose.yaw=count;
       ros::spinOnce();
       rate.sleep();

   }
   return 0;
}

