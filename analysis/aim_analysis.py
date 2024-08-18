import numpy as np
import serial
import time
from utils.geometry import BBox
from deep_models.detector.face_detector import face_detector
from utils.draw import (
    draw_plus,
    draw_bbox
    )


class AimController:
    def __init__(self, frame_shape):
        self.frame_shape = frame_shape
        self.frame_bbox = BBox([0,0,frame_shape[0],frame_shape[1]])
        
        self.face_detector = face_detector
        
        self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
        self.x_angle = 90
        self.y_angle = 0
        self.push_angle(x_angle=self.x_angle, y_angle=self.y_angle)
    
    def handle(self, frame):
        
        dets = self.face_detector.process(frame)
        
        if dets.shape[0]!=0:
            max_area_bbox = self.max_area_bbox(dets)
            
            self.compute_angles(max_area_bbox, self.frame_bbox)
            draw_bbox(frame, dets, color=(0,0,255), thickness=2, show=True)
            draw_plus(frame,self.frame_bbox.center, (255,150,0),30,4)
        self.push_angle(x_angle=self.x_angle, y_angle=self.y_angle)
        
        return frame

    def compute_angles(self, bbox:BBox, frame_bbox:BBox, thr:int=10):
        
        diff_x, diff_y = self.target_lock(bbox, frame_bbox)
        
        if abs(diff_x) > thr:
            diff_x_angle = int(diff_x / frame_bbox.width * 70)
            self.x_angle += diff_x_angle
            
        if self.x_angle < 0:
            self.x_angle = 0
        elif self.x_angle > 180:
            self.x_angle = 180
        
        print(f"X angle: {self.x_angle}")
        self.y_angle = int(diff_y / frame_bbox.height * 180)
        
        
    
    def target_lock(self, bbox:BBox, frame_bbox:BBox, thr:int=25):
        
        diff_x = frame_bbox.center[0] - bbox.center[0]
        diff_y = frame_bbox.center[1] - bbox.center[1]
                
        return diff_x, diff_y
    
    def choose_closest_bbox(self, dets, frame_bbox):
        
        min_distance = 1000000
        closest_bbox = BBox(dets[0,:4])
        
        for det in dets:
            bbox = BBox(det[:4])
            distance = np.linalg.norm(bbox.center - frame_bbox.center)
            if distance < min_distance:
                min_distance = distance
                closest_bbox = bbox
        
        return closest_bbox
    
    def max_area_bbox(self, dets):
            
        max_area = 0
        max_area_bbox = BBox(dets[0,:4])
        
        for det in dets:
            bbox = BBox(det[:4])
            area = bbox.area
            if area > max_area:
                max_area = area
                max_area_bbox = bbox
        
        return max_area_bbox
        
    def push_angle(self, x_angle, y_angle):
        angle = x_angle
        if type(angle)==int:
            angle_value = int(angle)
            if 0 <= angle_value <= 180:
                data = self.write_read(angle_value)
                if data:
                    print(f"Received: {data}")
            else:
                print("Açı 0 ile 180 arasında olmalıdır.")
        else:
            print("Lütfen geçerli bir sayı girin.")
    
    def write_read(self, x):
        try:
            self.arduino.write(bytes([x]))  # Tek bayt olarak veri gönder
            time.sleep(0.05)
            data = self.arduino.readline().decode('utf-8').strip()
            return data
        except serial.SerialException as e:
            print(f"SerialException: {e}")
            return None