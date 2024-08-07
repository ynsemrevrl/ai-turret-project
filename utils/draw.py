import cv2
import numpy as np

def draw_plus(frame:np.ndarray, 
              point_center:np.ndarray, 
              color = (255,255,255), line_thickness=2, length=10):
    
    center_x, center_y = point_center.astype(np.int32)

    frame[center_y-line_thickness : center_y+line_thickness, 
          center_x - length // 2 : center_x + length // 2 + 1,:] = color

    frame[center_y - length // 2 : center_y + length // 2 + 1, 
          center_x-line_thickness : center_x+line_thickness,:] = color

    