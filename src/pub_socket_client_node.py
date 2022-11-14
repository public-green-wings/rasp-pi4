import rospy
import socketio
import json
import numpy as np
from std_msgs.msg import String

from geographic_msgs.msg import GeoPoseStamped
from geometry_msgs.msg import PoseStamped, Vector3
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import GlobalPositionTarget

def image_cb(msg):
	sio.emit("IMG_MESSAGE",msg.data,namespace='/realtime')

host = "http://125.6.39.158:5001"

sio = socketio.Client()
#msg = GeoPoseStamped() #for global
msg = PoseStamped()

#pub = rospy.Publisher('targeting',GeoPoseStamped,queue_size=10) #for global
pub = rospy.Publisher('targeting',PoseStamped,queue_size=10)
#sub = rospy.Subscriber("my_camera",CompressedImage,image_cb)

rospy.init_node('pub_socket_client_node_', anonymous=True)

@sio.on('connect',namespace='/realtime')
def connect():
	sio.emit("REQ_MESSAGE",namespace='/realtime')

@sio.on('RES_MESSAGE',namespace='/realtime')
def receive_message(data):
	rospy.loginfo("Target Received")
	msg.header.stamp = rospy.Time.now()
	"""
	msg.pose.position.latitude = data['lat']
	msg.pose.position.longitude = data['long']
	msg.pose.position.altitude= data['alt']
	"""
	msg.pose.position.x = data['lat']
	msg.pose.position.y = data['long']
	msg.pose.position.z= data['alt']
	pub.publish(msg)
	sio.emit("REQ_MESSAGE",namespace='/realtime')


if __name__ == "__main__" :
	sio.connect(host,namespaces=['/realtime'])
		
