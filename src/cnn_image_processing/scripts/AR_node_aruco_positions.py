#!/usr/bin/env python3

import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2 as cv
import numpy as np
import imageio
from cnn_image_processing.msg import ArucoCornerCoordinates # custom msg

class Nodo(object):
    def __init__(self):
        # Parámetros
        self.image = None
        self.br = CvBridge()
        # Tasa de ciclo del nodo (en Hz).
        self.loop_rate = rospy.Rate(10)

        # Subscriptores
        rospy.Subscriber("/camera/color/image_raw", Image, self.callback)

        # Publicadores
        self.pub = rospy.Publisher('/ar_image', Image, queue_size=10)
        self.pub_aruco = rospy.Publisher('/aruco_corners', ArucoCornerCoordinates, queue_size=10)

        # Lista de códigos ArUco de interés
        self.aruco_codes = [0, 1, 2]  # IDs de los códigos ArUco de interés

        # Lista de rutas de los GIFs asociados a cada código ArUco
        self.gif_paths = [
            r'/home/husarion/GammaBot/src/cnn_image_processing/resources/0.gif',
            r'/home/husarion/GammaBot/src/cnn_image_processing/resources/1.gif',
            r'/home/husarion/GammaBot/src/cnn_image_processing/resources/2.gif'
        ] 

        # Cargar los GIFs asociados a cada código ArUco
        self.gifs = [imageio.get_reader(path) for path in self.gif_paths]
        self.gif_lengths = [gif.get_length() for gif in self.gifs]
        self.frame_indices = [0] * len(self.gifs)

        # Crear el objeto ArUco
        self.dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
        self.parameters = cv.aruco.DetectorParameters()
        self.detector = cv.aruco.ArucoDetector(self.dictionary, self.parameters)

        # Dimensiones conocidas del marcador
        self.marker_length = 0.1  # Ajusta según el tamaño real del marcador en metros

    def callback(self, msg):
        self.image = self.br.imgmsg_to_cv2(msg)

    def start(self):
        rospy.loginfo('Starting AR node...')
        
        while not rospy.is_shutdown():
            frame = self.image
            
            if frame is not None:
                # Detección de marcadores ArUco
                markerCorners, markerIds, _ = self.detector.detectMarkers(frame)
                frame_ = frame.copy()
                
                for code_idx, aruco_code in enumerate(self.aruco_codes):
                    if markerIds is not None and aruco_code in markerIds:
                        # Obtener la posición del marcador detectado
                        idx = list(markerIds).index(aruco_code)
                        img_points = markerCorners[idx][0]
                        
                        # Publicacion de esquinas del codigo aruco
                        aruco_msg = ArucoCornerCoordinates()
                        aruco_msg.aruco_id = aruco_code
                        aruco_msg.corner.x = img_points[0, 0]
                        aruco_msg.corner.y = img_points[0, 1]
                        aruco_msg.width = int(img_points[:, 0].max() - img_points[:, 0].min())
                        aruco_msg.height = int(img_points[:, 1].max() - img_points[:, 1].min())
                        self.pub_aruco.publish(aruco_msg)

                        # Obtener las dimensiones del GIF y ajustar su posición
                        if aruco_code > 0: 
                            mult_factor = 2
                        else:
                            mult_factor = 4
                        gif_height = int(img_points[:, 0].max() - img_points[:, 0].min()) * mult_factor
                        gif_width = int(img_points[:, 1].max() - img_points[:, 1].min()) * mult_factor
                        x, y = np.int32(img_points.mean(axis=0))

                        # Leer el siguiente fotograma del GIF
                        gif_frame = self.gifs[code_idx].get_data(self.frame_indices[code_idx])
                        self.frame_indices[code_idx] += 1
                        self.frame_indices[code_idx] = self.frame_indices[code_idx] % self.gif_lengths[code_idx]

                        # Redimensionar el GIF al tamaño del marcador
                        gif_frame = cv.resize(gif_frame, (gif_width, gif_height))

                        # Zona a sustituir
                        a = max(0, int(np.floor(y - 3 / 4 * gif_height)))
                        b = min(frame.shape[0], int(np.floor(y + 1 / 4 * gif_height)))
                        c = max(0, int(np.floor(x - 1 / 2 * gif_width)))
                        d = min(frame.shape[1], int(np.floor(x + 1 / 2 * gif_width)))

                        # Zona a sustituir del GIF si se sale
                        gif_a = 0
                        gif_b = gif_height
                        gif_c = 0
                        gif_d = gif_width
                        if a == 0:
                            gif_a = -int(np.floor(y - 3 / 4 * gif_height))
                        gif_b = gif_a + b - a
                        if c == 0:
                            gif_c = -int(np.floor(x - 1 / 2 * gif_width))
                        gif_d = gif_c + d - c

                        gif_frame = gif_frame[gif_a:gif_b, gif_c:gif_d, :]

                        # Superponer el GIF sobre el frame
                        alpha_s = gif_frame.min(axis=2) / 255.0
                        alpha_s = cv.merge([alpha_s, alpha_s, alpha_s])
                        alpha_l = 1.0 - alpha_s
                        frame_[a:b, c:d, :] = (alpha_l * gif_frame) + (alpha_s * frame[a:b, c:d, :])

                self.pub.publish(self.br.cv2_to_imgmsg(frame_, encoding='rgb8'))
                
            self.loop_rate.sleep()

if __name__ == '__main__':
    rospy.init_node("ar_addition", anonymous=True)
    my_node = Nodo()
    my_node.start()
