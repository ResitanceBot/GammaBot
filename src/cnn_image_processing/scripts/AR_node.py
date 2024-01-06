#!/usr/bin/env python3
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
# import keyboard
import imageio

class Nodo(object):
    def __init__(self):
        # Params
        self.image = None
        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(10)

        # Subscribers
        rospy.Subscriber("/camera/color/image_raw",Image,self.callback)

        # Publishers
        self.pub = rospy.Publisher('/ar_image', Image,queue_size=10)


    def callback(self, msg):
        #rospy.loginfo('Image received...')
        self.image = self.br.imgmsg_to_cv2(msg)


    def start(self):
        
        rospy.loginfo('Starting AR node...')
        
        # Ruta del gif
        gif_path = r'/home/husarion/GammaBot/src/cnn_image_processing/resources/fire-png-gif-489.gif'
        gif = imageio.get_reader(gif_path)
        gif_length = gif.get_length()
        frame_index = 0

        # Crear el objeto ArUco
        dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
        parameters = cv.aruco.DetectorParameters()
        detector = cv.aruco.ArucoDetector(dictionary, parameters)
        
        # Dimensiones conocidas del marcador
        marker_length = 0.1  # Ajusta según el tamaño real del marcador en metros

        mtx = None
        dist = None
        
        while not rospy.is_shutdown():
            
            frame = self.image
            
            if frame is not None:
                # Detección de marcadores ArUco
                markerCorners, markerIds, _ = detector.detectMarkers(frame)
                #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

                if markerIds is not None and 0 in markerIds:
                    # Obtener la posición del primer marcador detectado
                    index = list(markerIds).index(0)

                    # Obtener puntos 2D del marcador detectado
                    img_points = markerCorners[index][0]

                    # Obtener las dimensiones del gif y ajustar su posición
                    gif_height = int(img_points[:,0].max()-img_points[:,0].min())*4
                    gif_width = int(img_points[:,1].max()-img_points[:,1].min())*4
                    x,y = np.int32(img_points.mean(axis=0))

                    # Leer el siguiente fotograma del gif
                    gif_frame = gif.get_data(frame_index)
                    frame_index += 1
                    frame_index = frame_index%gif_length

                    # Redimensionar el gif al tamaño del marcador
                    gif_frame = cv.resize(gif_frame, (gif_width, gif_height))

                    # Zona a sustituir
                    a = max(0,int(np.floor(y-3/4*gif_height)))
                    b = min(frame.shape[0],int(np.floor(y+1/4*gif_height)))
                    c = max(0,int(np.floor(x-1/2*gif_width)))
                    d = min(frame.shape[1],int(np.floor(x+1/2*gif_width)))

                    # Zona a sustituir del gif si se sale
                    gif_a = 0
                    gif_b = gif_height
                    gif_c = 0
                    gif_d = gif_width
                    if a == 0:
                        gif_a = -int(np.floor(y-3/4*gif_height))
                    gif_b = gif_a + b - a
                    if c == 0:
                        gif_c = -int(np.floor(x-1/2*gif_width))
                    gif_d = gif_c + d - c

                    gif_frame = gif_frame[gif_a:gif_b, gif_c:gif_d, :]
                    # Superponer el gif sobre el framec
                    alpha_s = gif_frame.min(axis=2) / 255.0
                    alpha_s = cv.merge([alpha_s,alpha_s,alpha_s])
                    alpha_l = 1.0 - alpha_s
                    frame[a:b, c:d, :] = (alpha_l * gif_frame) + (alpha_s * frame[a:b, c:d, :])
            
                self.pub.publish(self.br.cv2_to_imgmsg(frame, encoding='rgb8'))
                
            self.loop_rate.sleep()
            
if __name__ == '__main__':
    rospy.init_node("ar_addition", anonymous=True)
    my_node = Nodo()
    my_node.start()