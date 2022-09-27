import rospy
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np
import struct

#include <sensor_msgs/NavSatFix.h>
#sensor_msgs::NavSatFix current_pose;

rospy.init_node("pub_camera_node")
rate=rospy.Rate(100)
cap = cv2.VideoCapture(0)

msg  = CompressedImage()		
pub_camera = rospy.Publisher("my_camera",CompressedImage)

if __name__ == "__main__":
	while 1:
		b, frame = cap.read()
		if b:
			msg.header.stamp = rospy.Time.now()
			msg.format =  "jpeg"
			encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),10]
			msg.data = np.array(cv2.imencode('.jpg', frame, encode_param)[1]).tostring()
			pub_camera.publish(msg)
		else : 
			pass
		rate.sleep()
	
