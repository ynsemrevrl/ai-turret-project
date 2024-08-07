from utils.geometry import BBox

def target_lock(bbox:BBox, frame_bbox:BBox, thr:int=100):
    
    x_movement_dict = {-1:"Sol",0: "Sabit",1:"Sağ"}
    y_movement_dict = {-1:"Aşağı",0: "Sabit",1:"Yukarı"}
    
    diff_x = frame_bbox.center[0] - bbox.center[0]
    diff_y = frame_bbox.center[1] - bbox.center[1]
    
    if abs(diff_x) > thr:
        if diff_x > 0:
            x_movement = -1
        elif diff_x < 0:
            x_movement = 1
        else:
            x_movement = 0
    else:
        x_movement=0
    
    if abs(diff_y) > thr:
        if diff_y > 0:
            y_movement = -1
        elif diff_y < 0:
            y_movement = 1
        else:
            y_movement = 0
    else:
        y_movement=0
    
    return x_movement, y_movement