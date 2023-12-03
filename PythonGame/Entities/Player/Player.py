from TickedObject import TickedObject
from Transform import Transform
from Vector import Vector
from Entities.Projectiles.Bullet import Bullet
from Behaviours.Movement import Movement
from Behaviours.Rotator import Rotator
from Shapes.Shape import Shape
from pygame.color import Color
import math
import pygame
import Game
import Input

class Player(TickedObject):
    def __init__(self, screen, transform:Transform):
        self.movement = Movement(transform, 1.0)
        self.shotPoint = Transform(Vector(0, 0), Vector(0, 0))
        self.rotation = Rotator(transform)
        cExpression = lambda:Color(0, 255, 0, 255)
        self.currentShape = Shape("Coolship", cExpression)
        self.shoot = False
        super().__init__(screen, transform)

    def setShotPointTransform(self):
        posVec = self.transform.position + (self.transform.getForward() * 0.5 * Game.unitScale)
        self.shotPoint = posVec

    def tick(self, deltaTime):
        self.currentShape.drawShape(self.screen, [self.transform.position.x, self.transform.position.y], 2.5, self.transform.zAngle - 90)
        self.movement.tick(deltaTime)
        self.rotation.tick()

        self.setShotPointTransform()

        if Input.getKeyState(pygame.K_SPACE) and self.shoot == False:
            Game.objmngr.InstanceQueue.append(Bullet(self.screen, Transform(Vector(0, 0), Vector(0, 0)), self.shotPoint, self.transform.getForward(), 0.1))
            self.shoot = True
        elif Input.getKeyState(pygame.K_SPACE) == False:
            self.shoot = False

        return super().tick(deltaTime)