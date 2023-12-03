from Transform import Transform
from Vector import Vector
import pygame
import Input
import math

class Rotator:
    def __init__(self, Transform:Transform):
        self.transform = Transform
        pass

    def tick(self):
        mousePos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        angle = math.atan2(mousePos.y - self.transform.position.y, mousePos.x - self.transform.position.x)
        self.transform.setAngle(math.degrees(angle))