#!/usr/bin/env python3

import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
from cnn_image_processing.msg import ArucoCornerCoordinates # custom msg

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
        self.pub = rospy.Publisher('/depth_image', Image,queue_size=10)

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
                # self.pub.publish(self.br.cv2_to_imgmsg(image_depth, encoding='16UC1'))
                if self.aruco is not None:
                    x = int(self.aruco.corner.x)
                    y = int(self.aruco.corner.y)
                    width = int(self.aruco.width)
                    height = int(self.aruco.height)
                    image_depth = self.image.copy()
                    area_aruco = image_depth[y:y+height, x:x+width]
                    dist_media_aruco = np.mean(area_aruco)
                    print('Aruco ID:', self.aruco.aruco_id)
                    print('Distancia (cm):', int(dist_media_aruco/10))
                    self.aruco = None
            
            self.loop_rate.sleep()
            
if __name__ == '__main__':
    
    rospy.init_node("depth_node", anonymous=True)
    my_node = Nodo()
    my_node.start()
