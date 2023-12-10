import pygame
from Entities.Foundation.ObjectManager import ObjectManager
from Entities.Foundation.EnemySpawner import EnemySpawner
from TickedObject import TickedObject
from Entities.Player.Player import Player
from Transform import Transform
from Vector import Vector
from Entities.ParticleSystem import ParticleSystem
from Entities.ParticleSystem import ParticleSystemEmission
import math

def InstantiateObject(obj:TickedObject):
    global instanceNumbers
    objectsAlive[instanceNumbers] = obj
    obj.setInstanceID(instanceNumbers)
    instanceNumbers += 1

def DestroyObject(obj:TickedObject):
    del objectsAlive[obj.instanceID]

objectsAlive = {}
instanceNumbers = 0
debug = False

# pygame setup
pygame.init()

worldOrigin = Vector(0, 0)
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True

pygame.display.set_caption("Invaderz")
pygame.display.set_icon(pygame.image.load("PythonGame/Assets/icon.png"))

# Instance Management
objmngr = ObjectManager(None, None)
spawner = EnemySpawner(screen, None, 2.0)
plr = Player(screen, Transform(Vector(100, 100), Vector(25, 25)))

objmngr.InstanceQueue.append(plr)
objmngr.InstanceQueue.append(spawner)

dt = 0
unitLength = 50.0
time = 0.0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    for obj in objectsAlive:
        objectsAlive[obj].tick(dt)
    
    objmngr.tick(dt)
    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = float(clock.tick(60)) / 1000.0 # limits FPS to 60
    time += dt

pygame.quit()