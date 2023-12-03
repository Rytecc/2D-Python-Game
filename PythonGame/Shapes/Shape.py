import pygame
from pygame.color import Color
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

        self.pointCoords = []
        for datum in self.rawShapeData:
            xy = datum.strip().split(',')
            self.pointCoords.append([float(xy[0]), float(xy[1])])

    # How can we incorporate rotation
    def drawShape(self, screen, center, nonUnitScale, zRotation):
        scale = nonUnitScale * Game.unitScale
        for i in range(0, self.pointCoords.__len__() - 1):
            pointAx = self.pointCoords[i][0] * scale
            pointAy = self.pointCoords[i][1] * scale

            pointBx = self.pointCoords[i + 1][0] * scale
            pointBy = self.pointCoords[i + 1][1] * scale

            #Convert pointCoords to polar coordinates
            pointAPolarR = math.sqrt(pointAx * pointAx + pointAy * pointAy)
            pointAPolarA = math.degrees(math.atan2(pointAy, pointAx))

            pointBPolarR = math.sqrt(pointBx * pointBx + pointBy * pointBy)
            pointBPolarA = math.degrees(math.atan2(pointBy, pointBx))

            #Add angle to polar coordinates
            pointAPolarA += zRotation
            pointBPolarA += zRotation

            #Revert back to cartesian coordinates
            pointAx = center[0] + pointAPolarR * math.cos(math.radians(pointAPolarA))
            pointAy = center[1] + pointAPolarR * math.sin(math.radians(pointAPolarA))

            pointBx = center[0] + pointBPolarR * math.cos(math.radians(pointBPolarA))
            pointBy = center[1] + pointBPolarR * math.sin(math.radians(pointBPolarA))

            pygame.draw.aaline(screen, self.colorExpression(), pygame.Vector2(pointAx, pointAy), pygame.Vector2(pointBx, pointBy))