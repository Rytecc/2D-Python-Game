from Transform import Transform
from typing import Callable
from TickedObject import TickedObject
from Vector import Vector
from pygame import Color
from Utility import Math
import math
import random
import pygame
import Game

class Particle:
    def __init__(self, spawnTime:float, originPoint:Vector, transform:Transform, positionFunction:Callable[[Transform, float], Vector], scaleFunction:Callable[[float], Vector], lifeTimeFunction:Callable[[float], float], colorExpression:Callable[[float], Color]) -> None:
        self.transform = transform

        self.lifeTimeExpression:Callable[[], float] = lifeTimeFunction
        self.posExpression:Callable[[Transform, float], Vector] = positionFunction
        self.scaleExpression:Callable[[float], Vector] = scaleFunction
        self.colorExpression:Callable[[float], Color] = colorExpression
        self.spawnTime = spawnTime
        self.origin = originPoint

class ParticleSystemEmission:
    def __init__(self, innerRadius, outerRadius, sweepAngle, emitRate) -> None:
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.sweepAngle = sweepAngle
        self.emitRate = emitRate
        pass
    
    def getEmitPosition(self, forwardVector:Vector) -> Vector:
        randMagnitude = random.random()
        randAngle = random.random()
        vectorMagnitude = (self.innerRadius + (self.outerRadius - self.innerRadius)) * randMagnitude
        vectorAngle = Math.lerp(-self.sweepAngle, self.sweepAngle, randAngle)
        return (forwardVector * vectorMagnitude * Game.unitLength).rotateVector(vectorAngle)
    

class ParticleSystem(TickedObject):
    def __init__(self, screen, Transform:Transform, posFunction:Vector, scaleFunction:float, lifeTimeFunction:float, colorFunction:Color, isLocal:bool, emitSettings:ParticleSystemEmission):
        self.particles:list[Particle] = []
        self.posFunction = posFunction
        self.scaleFunction = scaleFunction
        self.lifeTimeFunction = lifeTimeFunction
        self.colorFunction = colorFunction
        
        self.emitSettings = emitSettings
        self.isLocal = isLocal
        self.isPlaying = False
        
        self.timeLeft = 1.0 / emitSettings.emitRate
        super().__init__(screen, Transform)
    
    def tick(self, deltaTime):
        if self.timeLeft > 0 and self.isPlaying:
            self.timeLeft -= deltaTime
        elif self.timeLeft <= 0 and self.isPlaying:
            self.emit(1)
            self.timeLeft = 1.0 / self.emitSettings.emitRate
        
        i = self.particles.__len__() - 1
        while(i >= 0):
            currParticle = self.particles[i]
            timeAlive = Game.time - currParticle.spawnTime
            
            if timeAlive >= currParticle.lifeTimeExpression(timeAlive):
                self.particles.remove(currParticle)
                i -= 1
                continue
            
            newPosition = (self.transform.position + currParticle.origin if self.isLocal else currParticle.origin) + currParticle.posExpression(currParticle.transform, timeAlive)
            newScale = currParticle.scaleExpression(timeAlive)
            currParticle.transform.setPosition(newPosition)

            rectPos = Vector(newPosition.x + newScale.x * 0.5, newPosition.y + newScale.y * 0.5)
            pygame.draw.rect(self.screen, currParticle.colorExpression(timeAlive), [rectPos.x, rectPos.y, newScale.x, newScale.y])
            i -= 1
        
        super().tick(deltaTime)
    
    def emit(self, amount:int):
        for i in range(0, amount):
            origin = self.emitSettings.getEmitPosition(self.transform.getForward())
            if self.isLocal == False:
                origin += self.transform.position
            
            newTransform = Transform(Vector(0, 0), Vector(0, 0))
            newTransform.setForward(origin.normalize())
            self.particles.append(Particle(Game.time, origin, newTransform, self.posFunction, self.scaleFunction, self.lifeTimeFunction, self.colorFunction))
            
    def emitAtPosition():
        pass
    
    def reset(self):
        self.timeLeft = 1.0 / self.emitSettings.emitRate
        self.particles.clear()
        
    def setRunning(self, running:bool):
        self.isPlaying = running