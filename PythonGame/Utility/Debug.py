import pygame
import Vector
import Game

def debugCircle(screen, pVector:Vector.Vector, r:float):
    position = pVector * Game.unitLength
    radius = r * Game.unitLength
    pygame.draw.ellipse(screen, "white", [position.x - radius, position.y - radius, radius*2, radius*2])