import rospy
import socketio
import json
import numpy as np
from std_msgs.msg import String

from geographic_msgs.msg import GeoPoseStamped
from geometry_msgs.msg import PoseStamped, Vector3
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import GlobalPositionTarget

import eventlet

host = "http://125.6.39.158:5001"

sio = socketio.Client()
msg = GeoPoseStamped() #for global
#msg = PoseStamped() #for local
global_msg = NavSatFix()


def image_cb(msg):
	sio.emit("IMG_MESSAGE",msg.data,namespace='/realtime')

def global_cb(msg):
	global global_msg
	global_msg = msg


pub = rospy.Publisher('targeting',GeoPoseStamped,queue_size=10) #for global
#pub = rospy.Publisher('targeting',PoseStamped,queue_size=10) #for local
#sub = rospy.Subscriber("mavros/global_position/global",NavSatFix,global_cb)
#sub = rospy.Subscriber("mavros/local_position/pose",NavSatFix,global_cb)
#sub = rospy.Subscriber("my_camera",CompressedImage,image_cb)

rospy.init_node('pub_socket_client_node_', anonymous=True)
rate = rospy.Rate(0.3)

@sio.on('connect',namespace='/realtime')
def connect():
	sio.emit("JOIN",{"type":"DRONE"},namespace='/realtime')
	#sio.emit("REQ_MESSAGE",{"lat":global_msg.latitude, "long":global_msg.longitude, "alt":global_msg.altitude},namespace='/realtime')

@sio.on('REQ_POS',namespace='/realtime')
def receive_message(data):
	rospy.loginfo("Target Received")
	msg.header.stamp = rospy.Time.now()

	msg.pose.position.latitude = data['lat']
	msg.pose.position.longitude = data['long']
	msg.pose.position.altitude= data['alt']

	pub.publish(msg)

if __name__ == "__main__" :
	sio.connect(host,namespaces=['/realtime'],wait_timeout=15)

	while not rospy.is_shutdown():
		rospy.loginfo("EMIT!")
		sio.emit("CUR_POS",{"lat":global_msg.latitude, "long":global_msg.longitude, "alt":global_msg.altitude},namespace='/realtime')
		eventlet.sleep(0)
		rospy.loginfo("EMIT DONE!")
		rate.sleep()
		rospy.loginfo("EMIT FINISHED!")
