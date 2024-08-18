

from ultralytics import YOLO
from config import DETECTOR_CONFIG


class FaceDetector():
    def __init__(self, cfg):
        self.model = YOLO(cfg['model-path'])
        self.cfg = cfg
        
    def process(self, frame):
        
        results = self.model(frame, imgsz=self.cfg['img-size'], conf=self.cfg['conf'],
                        iou=self.cfg['iou'], show=False, verbose=False)
        
        return results[0].boxes.data.cpu().numpy().astype(int)
        

face_detector = FaceDetector(DETECTOR_CONFIG)