import numpy as np
from math import fabs, atan2, pi


class BBox():
    def __init__(self, coords):
        self._coords = coords

    @property
    def coords(self):
        return self._coords

    @property
    def center(self):
        return np.array([(self._coords[0] + self._coords[2])/2, (self._coords[1] + self._coords[3])/2])

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
    
    @property
    def width(self):
        return fabs(self._coords[2] - self._coords[0])
    
    @property
    def height(self):
        return fabs(self._coords[3] - self._coords[1])
    
    @property
    def area(self):
        return self.width * self.height


class KeyPoints():
    def __init__(self, keypoints: np.ndarray):

        self._keypoints = keypoints

    @property
    def points(self):
        return self._keypoints

    def point_xy(self, idx):

        self._idx = idx
        self.x = self._keypoints[self._idx][0]
        self.y = self._keypoints[self._idx][1]

        return (self.x, self.y)

    def calc_angle(self, p1, p2, p3) -> float:

        v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
        v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])

        v1_magnitude = np.linalg.norm(v1)
        v2_magnitude = np.linalg.norm(v2)

        dot_product = np.dot(v1, v2)

        cos_theta = dot_product / (v1_magnitude * v2_magnitude)

        angle = np.degrees(np.arccos(cos_theta))

        return angle

    def delta_xy(self, p1, p2) -> float:

        delta_x = p1[0] - p2[0]
        delta_y = p1[1] - p2[1]

        return (delta_x, delta_y)
