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
        self.loop_rate = rospy.Rate(1)

        # Subscribers
        rospy.Subscriber("/camera/depth/image_raw", Image, self.callback)

        # Matplotlib setup for real-time display
        plt.ion()  # Modo interactivo
        self.fig, self.ax = plt.subplots()  # Crea una figura y ejes

    def callback(self, msg):
        rospy.loginfo('Depth Image received...')
        self.image = self.br.imgmsg_to_cv2(msg, 'passthrough')  # Convierte a escala de grises directamente

    def start(self):
        rospy.loginfo("Starting depth image display")

        while not rospy.is_shutdown():
            if self.image is not None:
                # Muestra la imagen de profundidad con Matplotlib
                self.ax.imshow(self.image, cmap='jet')  # Puedes cambiar 'jet' por otro mapa de colores si prefieres
                self.fig.canvas.draw()  # Actualiza la figura
                self.fig.canvas.flush_events()  # Espera a que la GUI de Matplotlib responda

            self.loop_rate.sleep()

if __name__ == '__main__':
    rospy.init_node("depth_image_display", anonymous=True)
    my_node = Nodo()
    my_node.start()
