from TickedObject import TickedObject
from Vector import Vector
from Transform import Transform
import Game
import pygame
from Shapes.Shape import Shape
from Utility import Physics
from pygame.color import Color

class Bullet(TickedObject):
    def __init__(self, screen, transform:Transform, initPosition:Vector, direction:Vector, speed:float):
        self.initPosition = initPosition
        self.direction = direction
        self.speed = speed * Game.unitLength
        self.screen = screen
        self.shape = Shape("Bullet", lambda:Color(0, 255, 0, 255))
        transform.setPosition(initPosition)
        return super().__init__(screen, transform)
    
    def tick(self, deltaTime:float):
        self.transform.Translate(self.direction * self.speed * deltaTime)
        self.shape.drawShape(self.screen, self.transform.position.toArray(), 0.25, 0.0)

        if self.transform.position.x >= self.screen.get_width() or self.transform.position.x <= 0:
            self.dispose()
        elif self.transform.position.y >= self.screen.get_height() or self.transform.position.y <= 0:
            self.dispose()

        overlaps = Physics.overlapCircle(self.transform.position, 25.0)

        for overlap in overlaps:
            if overlap.tags.__contains__("Enemy") == False:
                continue

            self.dispose()
            overlap.interact(1.0, "Damage")
            break

        return super().tick(deltaTime)
