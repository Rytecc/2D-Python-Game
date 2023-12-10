import pygame
from pygame.color import Color
from Vector import Vector
import math
import Game
import os

shapesPath = os.path.dirname(os.path.abspath(__file__))

class Shape:
    def __init__(self, shapeName, colorExpression:Color) -> None:
        self.shapeFile = f"{shapesPath}\\{shapeName}.shape"
        self.colorExpression = colorExpression
        shapeDataStream = open(self.shapeFile, "r")
        
        self.rawShapeData = shapeDataStream.readlines()
        self.pointArray = []
        for datum in self.rawShapeData:
            xy = datum.strip().split(',')
            self.pointArray.append(Vector(float(xy[0]), float(xy[1])))

    def calculatePoint(self, point:Vector, center:Vector, nonUnitScale:float, zRotation:float) -> Vector:
        radianAngle = math.radians(zRotation)
        x = point.x * math.cos(radianAngle) - point.y * math.sin(radianAngle)
        y = point.x * math.sin(radianAngle) + point.y * math.cos(radianAngle)
        return center + Vector(x, y) * (nonUnitScale * Game.unitLength)

    def drawShape(self, screen, center, nonUnitScale, zRotation):
        for i in range(0, self.pointArray.__len__() - 1):
            aPoint = self.calculatePoint(self.pointArray[i], Vector(center[0], center[1]), nonUnitScale, zRotation)
            bPoint = self.calculatePoint(self.pointArray[i + 1], Vector(center[0], center[1]), nonUnitScale, zRotation)
            pygame.draw.aaline(screen, self.colorExpression(), [aPoint.x, aPoint.y], [bPoint.x, bPoint.y])