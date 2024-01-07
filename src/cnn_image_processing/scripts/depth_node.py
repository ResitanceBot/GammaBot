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
        print('Aruco ID:',msg.aruco_id)

    def start(self):
        rospy.loginfo("Starting depth node")
        image_processed = self.image
        
        while not rospy.is_shutdown():
            if image_processed is not None:
                # Muestra la imagen procesada de profundidad
                self.pub.publish(self.br.cv2_to_imgmsg(image_processed, encoding='16UC1'))
               
            self.loop_rate.sleep()
            
if __name__ == '__main__':
    rospy.init_node("depth_node", anonymous=True)
    my_node = Nodo()
    my_node.start()
