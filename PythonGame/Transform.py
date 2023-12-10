from Vector import Vector
import pygame
import Game
import math

class Transform:
    def __init__(self, pVector:Vector, sVector:Vector):
        self.position = pVector
        self.scale = sVector
        self.zAngle = 0

    def Translate(self, dpVector:Vector):
        self.position.x += dpVector.x
        self.position.y += dpVector.y

    def setPosition(self, pVector:Vector):
        self.position = pVector

    def setScale(self, sVector:Vector):
        self.scale = sVector

    def Rotate(self, dA):
        self.zAngle += dA

    def setAngle(self, a):
        self.zAngle = a
    
    def setForward(self, fwd:Vector):
        self.forwardVector = fwd.normalize()
        self.zAngle = math.degrees(math.atan2(self.forwardVector.y, self.forwardVector.x))
    
    def getForward(self) -> Vector:
        resX = 0.0
        resY = 0.0

        radZ = math.radians(self.zAngle)
        resX = math.cos(radZ)
        resY = math.sin(radZ)

        forwardVec = Vector(resX, resY)
        posWithForward = self.position + (forwardVec * 25.0)
        if Game.debug: 
            pygame.draw.line(Game.screen, "green", [self.position.x, self.position.y], [posWithForward.x, posWithForward.y])

        return Vector(resX, resY)
    
    def copy(self):
        return Transform(self.position, self.scale)