from Vector import Vector
from TickedObject import TickedObject
import Game
import pygame

def overlapCircle(center:Vector, radius:float) -> list[TickedObject]:
    entities = list[TickedObject](Game.objectsAlive.values())
    x = entities.__len__() - 1
    while x >= 0:

        if entities[x].transform != None and (entities[x].transform.position - center).magnitude() > radius:
            del entities[x]

        x -= 1

    return entities