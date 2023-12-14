from Transform import Transform
from TickedObject import TickedObject
from Vector import Vector
from Shapes.Shape import Shape
from Entities.Particles.ParticleSystem import ParticleSystem
from Entities.Particles.ParticleSystem import ParticleSystemEmission
from Entities.Powerups.FirerateBuff import FireRateBuff
from Utility import Physics
import pygame
import math
import Game

class FirerateDrop(TickedObject):
    def __init__(self, screen, Transform: Transform):
        super().__init__(screen, Transform)
        self.boundShape = Shape("Circle", lambda : "white")
        self.spawnTime = Game.time

        # All Values are tweaked through testing
        lifeTimeFunction = lambda tA : 0.5
        posFunction = lambda tr, tA, nC : (tr.getForward() * 0.5) * (tA / lifeTimeFunction(1.0)) * -Game.unitLength
        scaleFunction = lambda tA, nC : (Vector(1.0, 1.0) * ((1.0 - tA / lifeTimeFunction(1.0)) * 0.15)) * Game.unitLength
        colorFunction = lambda tA : pygame.Color(255, 0, 0, 255)

        emitSettings = ParticleSystemEmission(0.45, 0.5, 180.0, 75.0)
        self.aura = ParticleSystem(screen, self.transform.copy(), posFunction, scaleFunction, lifeTimeFunction, colorFunction, True, emitSettings, False)
        self.aura.setRunning(True)

    def tick(self, deltaTime):
        self.aura.isPlaying = True
        self.aura.tick(deltaTime)
        overlaps = Physics.overlapCircle(self.transform.position, 1.0 * Game.unitLength, "Player")

        if overlaps.__len__() > 0:
            overlaps[0].interact(FireRateBuff(5.0, 3.0), "Powerup")
            self.dispose()
        
        super().tick(deltaTime)