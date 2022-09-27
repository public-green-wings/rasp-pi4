import rospy
from std_msgs.msg import String
import json
import urllib
from urllib.request import Request, urlopen
from geographic_msgs.msg import GeoPoseStamped
from sensor_msgs.msg import NavSatFix
#include <sensor_msgs/NavSatFix.h>
#sensor_msgs::NavSatFix current_pose;

target_list =  []

def get_optimal_route(start, goal, waypoints=['',''], option='') :
	
    client_id = 'un9kcwrg1q'
    client_secret = 'siQivhiLqX0w2R6BVyYV2Z6HHbvk3nsh66K3jLtu' 
    # start=/goal=/(waypoint=)/(option=) 순으로 request parameter 지정
    url = f"https://naveropenapi.apigw.ntruss.com/map-direction-15/v1/driving?start={start[0]},{start[1]}&goal={goal[0]},{goal[1]}&option={option}"
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    
    response = urllib.request.urlopen(request)
    res = response.getcode()
    
    if (res == 200) :
        response_body = response.read().decode('utf-8')
        ret = json.loads(response_body)
        return ret['route']['traoptimal'][0]['path']
  
  
def locate_cb(msg):
	global target_list
	#rospy.loginfo("Processing!")
	start=(str(current_gps.longitude), str(current_gps.latitude))
	end =(str(msg.pose.position.longitude),str(msg.pose.position.latitude))
	temp = get_optimal_route(start,end)
	target_list += temp
	#rospy.loginfo("Processed!")

def current_cb(msg):
	current_gps.latitude=msg.latitude
	current_gps.longitude = msg.longitude
	current_gps.altitude = msg.altitude



err= 0.0001

current_gps = NavSatFix()
target_msg = GeoPoseStamped()



rospy.init_node("pub_route_to_target_node")
rate=rospy.Rate(10)

rospy.Subscriber("locating",GeoPoseStamped,locate_cb)
rospy.Subscriber("/mavros/global_position/global",NavSatFix,current_cb)

pub_targeting = rospy.Publisher("targeting",GeoPoseStamped,queue_size=10)

	
# 주소에 geocoding 적용하는 함수를 작성.



#  함수 적용
if __name__ == "__main__":
	while 1:
		#rospy.loginfo("Processing!")
		if target_list:
			#rospy.loginfo("targeted!")
			target = target_list[0]
			#rospy.loginfo(f"Current:({current_gps.longitude},{current_gps.latitude}), Target:({target[0]},{target[1]})")
			if ((abs(float(target[0])-current_gps.longitude) < err) and (abs(float(target[1])-current_gps.latitude)<err)):
				#rospy.loginfo("INSIDE!")
				if len(target_list)==1 :
					target_list=[]
				else :
					target_list = target_list[1:]
			else :
				target_msg.header.stamp = rospy.Time.now()
				target_msg.pose.position.longitude = target[0]
				target_msg.pose.position.latitude = target[1]
				target_msg.pose.position.altitude = 600
				pub_targeting.publish(target_msg)

		rate.sleep()
