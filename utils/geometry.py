import numpy as np

class BBox():
    def __init__(self, coords):
        self._coords = coords

    @property
    def coords(self):
        return self._coords
    
    @property
    def center(self):
        return np.array([(self._coords[0] + self._coords[2])/2,(self._coords[1] + self._coords[3])/2 ])

    @property
    def tl(self):
        return np.array([self._coords[0:2]])
    
    @property
    def br(self):
        return np.array([self._coords[2:4]])
    
    @property
    def x1(self):
        return self._coords[0]
    
    @property
    def y1(self):
        return self._coords[1]
    
    @property
    def x2(self):
        return self._coords[2]
    
    @property
    def y2(self):
        return self._coords[3]
    
    
    
    