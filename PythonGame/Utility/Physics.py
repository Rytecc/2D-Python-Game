from Vector import Vector
from TickedObject import TickedObject
import Game
import pygame

def overlapCircle(center:Vector, radius:float, filter:str) -> list[TickedObject]:
    entities = list[TickedObject](Game.objectsAlive.values())
    x = entities.__len__() - 1

    while x >= 0:
        if entities[x].transform == None:
            del entities[x]
            x -= 1
            continue
        
        if (entities[x].transform.position - center).magnitude() > radius:
            del entities[x]
            x -= 1
            continue
        
        if filter != None and entities[x].tags.__contains__(filter) == False:
            del entities[x]
            x -= 1
            continue

        x -= 1

    return entities