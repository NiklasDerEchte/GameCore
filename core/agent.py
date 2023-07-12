from core.core import *
from core.math import *

class NavAgent:
    def __init__(self, position, speed=1):
        self.position = position
        self.speed = speed
        self.distance = 0

    def move(self, destination):
        delta_vec = (destination[0] - self.position[0], destination[1] - self.position[1])
        self.distance = math.sqrt((delta_vec[0] ** 2) + (delta_vec[1] ** 2))
        if self.distance > 0:
            new_pos_x = self.position[0] + (min(self.speed, round(self.distance)) * delta_vec[0] / self.distance)
            new_pos_y = self.position[1] + (min(self.speed, round(self.distance)) * delta_vec[1] / self.distance)
            self.position = (new_pos_x, new_pos_y)

