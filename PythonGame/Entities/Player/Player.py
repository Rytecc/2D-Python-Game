from TickedObject import TickedObject
from Transform import Transform
from Vector import Vector
from Behaviours.Movement import Movement
from Behaviours.Rotator import Rotator
from Shapes.Shape import Shape
from pygame.color import Color
import Entities.Particles.ParticleSystem as ParticleSystem
import pygame
import Game
import math
import Input

PLAYER_SPEED = 2.5

class Player(TickedObject):
    def __init__(self, screen, transform:Transform):
        super().__init__(screen, transform)
        self.movement = Movement(transform, PLAYER_SPEED)
        self.shotPoint = Transform(Vector(0, 0), Vector(0, 0))
        self.rotation = Rotator(transform)
        self.buffs:list[Buff] = []
        
        self.maxHealth = 25.0
        self.currentHealth = self.maxHealth
        
        cExpression = lambda:Color(int(255.0 * (1.0 - self.currentHealth / self.maxHealth)), int(255.0 * (self.currentHealth / self.maxHealth)), 0, 100)
        self.currentShape = Shape("Coolship", cExpression)
        self.shoot = False
        self.addTag("Player")
        
        self.weapon = Shotgun(self)
        
        auraLifeTimeFunc = lambda tA : 2.0
        auraPosFunc = lambda tr, tA, nC : tr.getForward() * (math.sinh(math.pow(tA/auraLifeTimeFunc(1.0),3)) * 2.5 * Game.unitLength)
        auraScaleFunc = lambda tA, nC : Vector(0.15, 0.15) * ((auraLifeTimeFunc(1.0) - tA) / auraLifeTimeFunc(1.0)) * Game.unitLength
        auraColorFunc = lambda tA : cExpression()
        
        auraSettings = ParticleSystem.ParticleSystemEmission(0, 1.0, 180.0, 100.0)
        self.aura = ParticleSystem.ParticleSystem(screen, self.transform.copy(), auraPosFunc, auraScaleFunc, auraLifeTimeFunc, auraColorFunc, True, auraSettings)

        expLifeTimeFunc = lambda tA : 0.5
        expPosFunc = lambda tr, tA, nC : tr.getForward() * Game.unitLength * 2.5 * (tA / expLifeTimeFunc(1.0)) * (1 + nC)
        expScaleFunc = lambda tA, nC : Vector(0.25, 0.25) * ((expLifeTimeFunc(1.0) - tA) / expLifeTimeFunc(1.0)) * Game.unitLength
        auraColorFunc = lambda tA : cExpression()
        self.explosion = ParticleSystem.ParticleSystem(screen, self.transform.copy(), expPosFunc, expScaleFunc, expLifeTimeFunc, auraColorFunc, False, auraSettings, False)

    def setShotPointTransform(self):
        posVec = self.transform.position + (self.transform.getForward() * 0.5 * Game.unitLength)
        self.shotPoint = posVec

    def tick(self, deltaTime):
        if self.disposed:
            return

        # Run player movement
        self.movement.tick(deltaTime)
        self.rotation.tick()

        # Tick Buffs
        buffIndex = self.buffs.__len__() - 1
        while(buffIndex >= 0):
            buff = self.buffs[buffIndex]
            buff.apply(self, deltaTime)
            
            if buff.alive == False:
                self.buffs.remove(buff)
                
            buffIndex -= 1
            
        # Run Aura Particle System based on buffs
        self.aura.setRunning(False if self.buffs.__len__() == 0 else True)
        self.explosion.setRunning(False)

        self.aura.tick(deltaTime)
        self.explosion.tick(deltaTime)

        # Determine values for player scale for pulse effect with respect to health
        strobeSpeed = self.maxHealth / (0.05 if self.currentHealth <= 0.0 else self.currentHealth)
        scaleExpression = 1.5 + (math.sin(strobeSpeed * Game.time) * 0.1)
        
        # draw the player
        self.currentShape.drawShape(self.screen, [self.transform.position.x, self.transform.position.y], scaleExpression, self.transform.zAngle - 90)

        # Set the point position/orientation at which bullets will be shot
        self.setShotPointTransform()
        
        #Tick the player's current weapon
        self.weapon.run(deltaTime)
    
    def interact(self, args, type: str):
        if type == "Heal":
            self.currentHealth += args
        elif type == "Damage":
            self.currentHealth -= args
        elif type == "Powerup":
            self.addBuff(args)
        
        if self.currentHealth <= 0:
            self.dispose()
        
        return super().interact(args, type)
    
    def addBuff(self, newBuff):
        self.explosion.emit(50)
        self.buffs.append(newBuff)

from Entities.Powerups.Powerup import Buff

from Behaviours.Weapons.Shotgun import Shotgun
from Behaviours.Weapons.Basic import Basic