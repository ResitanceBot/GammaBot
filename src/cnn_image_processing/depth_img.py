#!/usr/bin/env python3
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np

class Nodo(object):
    def __init__(self):
        # Params
        self.image = None
        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(10)

        # Subscribers
        rospy.Subscriber("/camera/depth/image_raw",Image,self.callback)

        # Publishers
        self.pub = rospy.Publisher('/test/depth', Image,queue_size=10)

    def callback(self, msg):
        rospy.loginfo('Depth Image received...')
        self.image = self.br.imgmsg_to_cv2(msg,'16UC1')


    def start(self):
        rospy.loginfo("Timing images")
        
        while not rospy.is_shutdown():
            rospy.loginfo('processing image')
            image_processed = self.image
            
            if self.image is not None:
                rospy.loginfo('-------------------')
                
                # Procesar la imagen de profundidad
                max_depth_value = 2000  # Valor máximo permitido para la profundidad
                depth_image_processed = np.where(image_processed > max_depth_value, 0, image_processed)  # Píxeles lejanos se establecen a 0

                #cv2.imshow("Imagen", self.image)
                self.pub.publish(self.br.cv2_to_imgmsg(depth_image_processed, encoding='16UC1'))
                
            self.loop_rate.sleep()
            
if __name__ == '__main__':
    rospy.init_node("astra_image_processor", anonymous=True)
    my_node = Nodo()
    my_node.start()