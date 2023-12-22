from roboflow import Roboflow
import cv2
import matplotlib.pyplot as plt

rf = Roboflow(api_key="GGxqvKnwaHYEl42XKsup")
project = rf.workspace().project("fire-detection-for-khkt")
model = project.version(3).model

# Open a connection to the PC camera (adjust the camera index as needed)
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Make sure the frame is not None
    if frame is not None:
        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Make predictions on the frame
        predictions = model.predict(frame_rgb, confidence=40, overlap=30).json()

        # Print or process predictions as needed
        print(predictions)

        # Draw bounding boxes on the frame based on predictions
        for prediction in predictions["predictions"]:
            xmin, ymin, xmax, ymax = (
                int(prediction["x"]),
                int(prediction["y"]),
                int(prediction["x"] + prediction["width"]),
                int(prediction["y"] + prediction["height"]),
            )
            cv2.rectangle(frame_rgb, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        # Display the frame with predictions using matplotlib
        plt.imshow(frame_rgb)
        plt.show()

    

# Release the camera
cap.release()
