from roboflow import Roboflow
import cv2
import openni
import matplotlib.pyplot as plt
import numpy as np

rf = Roboflow(api_key="GGxqvKnwaHYEl42XKsup")
project = rf.workspace().project("fire-detection-for-khkt")
model = project.version(3).model

# Initialize OpenNI context and depth stream
ctx = openni.Context()
ctx.init()

# Abre la cámara Astra (ajusta el índice del dispositivo según sea necesario)
dev = ctx.devices[1]
depth_stream = dev.create_depth_stream()
depth_stream.start()

while True:
    # Captura un cuadro desde la cámara Astra
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    frame_array = np.ndarray((frame.height, frame.width), dtype=np.uint16, buffer=frame_data)

    # Convierte el cuadro a formato RGB
    frame_rgb = cv2.cvtColor(frame_array, cv2.COLOR_GRAY2RGB)

    # Realiza predicciones en el cuadro
    predictions = model.predict(frame_rgb, confidence=18, overlap=30).json()

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
        cv2.rectangle(frame_rgb, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    # Muestra el cuadro con las predicciones utilizando matplotlib
    plt.imshow(frame_rgb)
    plt.show()

# Detiene la transmisión de profundidad y libera la cámara Astra
depth_stream.stop()
depth_stream.destroy()
ctx.shutdown()
