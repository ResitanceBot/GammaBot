#!/usr/bin/env python3

import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
from cnn_image_processing.msg import ArucoCornerCoordinates # custom msg
from cnn_image_processing.msg import ArucoDistOri # custom msg
from math import asin, sin, degrees, radians

def angular_position(shape,y,x,fov=(60,49.5)):
    x_c = x-(shape[1]-1)/2
    y_c = (shape[0]-1)/2-y
    w_c = (shape[1]+1)/2
    h_c = (shape[0]+1)/2
    theta_max = fov[0]/2
    phi_max = fov[1]/2
    theta = degrees(asin(sin(radians(theta_max)/w_c*x_c)))
    phi = degrees(asin(sin(radians(phi_max)/h_c*y_c)))
    return theta,phi

class Nodo(object):
    def __init__(self):
        # Params
        self.image = None
        self.aruco = None
        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(10)

        # Subscribers
        rospy.Subscriber("/camera/depth/image_raw", Image, self.callback_img)
        rospy.Subscriber("/aruco_corners", ArucoCornerCoordinates, self.callback_aruco)
        
        # Publishers
        self.pub = rospy.Publisher('/aruco_dist_ori', ArucoDistOri, queue_size=10)

    def callback_img(self, msg):
        # rospy.loginfo('Depth Image received...')
        self.image = self.br.imgmsg_to_cv2(msg, 'passthrough')  # Convierte a escala de grises directamente
        
    def callback_aruco(self, msg):
        # print('Aruco ID:',msg.aruco_id)
        self.aruco = msg

    def start(self):
        rospy.loginfo("Starting depth node")
        
        while not rospy.is_shutdown():
            if self.image is not None:
                # rospy.loginfo('-------------------')
                if self.aruco is not None:
                    x = int(self.aruco.corner.x)
                    y = int(self.aruco.corner.y)
                    width = int(self.aruco.width)
                    height = int(self.aruco.height)
                    
                    image_depth = self.image.copy()
                    area_aruco = image_depth[y:y+height, x:x+width]
                    dist_media_aruco = np.mean(area_aruco)
                    
                    shape_img = (640, 480)
                    x_center = x + width/2
                    y_center = y + height/2
                    angle_aruco = angular_position(shape_img,x_center,y_center)
                    
                    # print('Aruco ID:', self.aruco.aruco_id)
                    # print('Distancia (cm):', int(dist_media_aruco/10))
                    # print('Pitch (º):', angle_aruco[0])
                    # print('Yaw (º):', angle_aruco[1])
                    # print('------------------------')
                    
                    aruco_msg = ArucoDistOri()
                    aruco_msg.aruco_id = self.aruco.aruco_id
                    aruco_msg.distance = int(dist_media_aruco)
                    aruco_msg.angle = int(angle_aruco[1])
                    self.pub.publish(aruco_msg)
                    
                    self.aruco = None
            
            self.loop_rate.sleep()
            
if __name__ == '__main__':
    
    rospy.init_node("depth_node", anonymous=True)
    my_node = Nodo()
    my_node.start()
