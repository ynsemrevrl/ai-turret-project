
import cv2
import numpy as np
import time
from analysis.aim_analysis import AimController
from utils.video_control import Controller

cap = cv2.VideoCapture(2)
fps = cap.get(5)
print(f"FPS: {fps}")

width = int(cap.get(3))
height = int(cap.get(4))

aim_controller = AimController((width, height))
video_controller = Controller()

frame_id = 0

while True:
    print("-"*50)
    success, frame = cap.read()

    if success:
        
        frame = aim_controller.handle(frame)
        
        is_break, key = video_controller.check()
        
        if is_break:
            break
        
        frame = np.flip(frame, axis=1)
        frame = cv2.resize(frame, (1920, 1080))
        cv2.namedWindow("Detections", cv2.WINDOW_NORMAL)
        cv2.imshow("Detections", frame)
    # time.sleep(0.05)
    frame_id += 1
    print("-"*50)

cap.release()
cv2.destroyAllWindows()
