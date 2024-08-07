from ultralytics import YOLO
from analysis.aim_analysis import target_lock
from utils.geometry import BBox
from utils.draw import draw_plus
from math import ceil
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
fps = cap.get(5)

width = cap.get(3)
height = cap.get(4)

frame_bbox = BBox([0,0,width,height])

model = YOLO("./weights/yolov8n-face.pt")

frame_id = 0
x_status,y_status = -1,-1

pause = False

while True:

    success, frame = cap.read()

    if success:
        
        results = model(frame, imgsz=640, conf=0.3,
                        iou=0.7, show=False, verbose=False)

        for r in results:
            bbox = r.boxes

            for box in bbox:
                
                x1, y1, x2, y2 = box.xyxy[0].cpu()
                bbox_cls = BBox([x1, y1, x2, y2])
                frame_bbox_center = frame_bbox.center.astype(np.int16)
                # if frame_id % fps ==0:
                x_status,y_status = target_lock(bbox_cls, frame_bbox, thr=30)
                
                if x_status == 0 and y_status == 0:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                
                conf = ceil(box.conf[0]*100)/100

                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # cv.rectangle(frame, 
                #              pt1=(frame_bbox_center[0]-50, frame_bbox_center[1]-50), 
                #              pt2=(frame_bbox_center[0]+50, frame_bbox_center[1]+50),
                #              color=(255,0,0), thickness=4)
                
                # cv.circle(frame,frame_bbox_center,10,(255,150,0),-1)
                # cv.circle(frame,bbox_cls.center.astype(np.int16),10,(255,150,0),-1)
                            
                cv.rectangle(frame, pt1=(x1, y1), pt2=(x2, y2),
                             color=color, thickness=4)
                cv.putText(frame, f"face {conf}", (x1, y1-5), color=color,
                           thickness=2, fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=0.7)
                
        draw_plus(frame,frame_bbox_center, (255,150,0),30,4)
        # draw_plus(frame, bbox_cls.center,(0,150,255),15,3)

        frame = np.flip(frame, axis=1)

        cv.imshow("Detections", frame)

        if pause:
            key = cv.waitKey(0)
        else:
            key = cv.waitKey(1)

        if key == ord("q"):
            print("Shutting Down!")
            break
        
        if key == ord("p"):
            if pause:
                pause=False
            else:
                pause=True
                
        
    frame_id += 1

cap.release()
cv.destroyAllWindows()
