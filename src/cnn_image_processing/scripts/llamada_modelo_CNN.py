import torch
#
#model = torch.jit.load('model_scripted.pt')
#model.eval()
import cv2
import supervision as sv
from ultralytics import YOLO


def main():
    
    # to save the video
    writer= cv2.VideoWriter('flower_corner_labeled.mp4', 
                            cv2.VideoWriter_fourcc(*'DIVX'), 
                            7, 
                            (1280, 720))
    
    # define resolution
    cap = cv2.VideoCapture("flower_corner.mp4")
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # specify the model
    model = YOLO("runs/detect/yolov8n_custom/weights/best.pt")

    # customize the bounding box
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )


    while True:
        ret, frame = cap.read()
        if ret:
            result = model(frame, agnostic_nms=True)[0]
            detections = sv.Detections.from_yolov8(result)
            print("detections", detections)
            labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for _, _, confidence, class_id, _
                in detections
                ]
            frame = box_annotator.annotate(
                scene=frame, 
                detections=detections, 
                labels=labels
                ) 
            
            writer.write(frame)
            
            cv2.imshow("yolov8", frame)
            
            if (cv2.waitKey(30) == 27): # break with escape key
                break
        else:
            break
            
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()