#!/usr/bin/env python3
import rospy
from roboflow import Roboflow
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import matplotlib.pyplot as plt

class Nodo(object):
    def __init__(self):
        # Params
        self.image = None
        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(10)

        # Subscribers
        rospy.Subscriber("/ar_image",Image,self.callback)

        # Publishers
        self.pub = rospy.Publisher('/pred_image', Image,queue_size=10)

        self.rf = Roboflow(api_key="GGxqvKnwaHYEl42XKsup")
        self.project = self.rf.workspace().project("fire-detection-for-khkt")
        self.model = self.project.version(3).model

    def callback(self, msg):
        rospy.loginfo('Image received...')
        self.image = self.br.imgmsg_to_cv2(msg)


    def start(self):
        rospy.loginfo("Timing images")
        #rospy.spin()
        while not rospy.is_shutdown():
            rospy.loginfo('processing image')
            #br = CvBridge()
            image_processed = self.image
            if self.image is not None:
                rospy.loginfo('alo alo image')
                    # Realiza predicciones en el cuadro
                predictions = self.model.predict(image_processed, confidence=30, overlap=30).json()

                # Imprime o procesa las predicciones según sea necesario
                print(predictions)

                # Dibuja cajas delimitadoras en el cuadro según las predicciones
                for prediction in predictions["predictions"]:
                    xmin, ymin, xmax, ymax = (
                        int(prediction["x"]),
                        int(prediction["y"]),
                        int(prediction["x"] + prediction["width"]),
                        int(prediction["y"] + prediction["height"]),
                    )
                    cv2.rectangle(image_processed, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                #cv2.imshow("Imagen", self.image)
                self.pub.publish(self.br.cv2_to_imgmsg(image_processed, encoding='rgb8'))
            self.loop_rate.sleep()
            
if __name__ == '__main__':
    rospy.init_node("astra_image_processor", anonymous=True)
    my_node = Nodo()
    my_node.start()