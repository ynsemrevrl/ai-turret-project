import cv2, random
import numpy as np

def draw_plus(frame:np.ndarray, 
              point_center:np.ndarray, 
              color = (255,255,255), line_thickness=2, length=10):
    
    center_x, center_y = point_center.astype(np.int32)

    frame[center_y-line_thickness : center_y+line_thickness, 
          center_x - length // 2 : center_x + length // 2 + 1,:] = color

    frame[center_y - length // 2 : center_y + length // 2 + 1, 
          center_x-line_thickness : center_x+line_thickness,:] = color
    

def plot_one_box(x, img, color=None, label=None, line_thickness=3):
      # Plots one bounding box on image img
      tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
      color = color or [random.randint(0, 255) for _ in range(3)]
      c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
      cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
      if label:
            tf = max(tl - 1, 1)  # font thickness
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
            cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        
def draw_bbox(frame, dets, color=(255,255,255), thickness=2, show=True):
      if show == False:
            return frame
      
      for det in dets:
            bbox = det[:4]
            # print(bbox.astype(np.int32))
            conf = det[4]
            #   label = f"face {conf}"
            label = ''

            plot_one_box(bbox, frame, color=color, label=label, line_thickness=thickness)
            

      
    