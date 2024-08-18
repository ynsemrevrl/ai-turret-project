
import cv2

class Controller():
    def __init__(self):
        self.is_break = False
        self.pause = False
    
    def check(self):
            
        if self.pause:
            key = cv2.waitKey(0)
        else:
            key = cv2.waitKey(1)
        
        if key == ord("p"):
            if self.pause:
                self.pause=False
            else:
                self.pause=True
                
        if key & 0xFF == ord('q'):
            self.is_break = True
            
        return self.is_break, key