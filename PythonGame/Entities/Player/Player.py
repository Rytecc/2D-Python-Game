from TickedObject import TickedObject
from Transform import Transform
from Vector import Vector
from Behaviours.Movement import Movement
from Behaviours.Rotator import Rotator
from Shapes.Shape import Shape
from pygame.color import Color
from Entities.ParticleSystem import ParticleSystem
from Entities.ParticleSystem import ParticleSystemEmission
import Game
import math

PLAYER_SPEED = 2.5

class Player(TickedObject):
    def __init__(self, screen, transform:Transform):
        super().__init__(screen, transform)
        self.movement = Movement(transform, PLAYER_SPEED)
        self.shotPoint = Transform(Vector(0, 0), Vector(0, 0))
        self.rotation = Rotator(transform)
        
        
        self.maxHealth = 25.0
        self.currentHealth = self.maxHealth
        
        cExpression = lambda:Color(int(255.0 * (1.0 - self.currentHealth / self.maxHealth)), int(255.0 * (self.currentHealth / self.maxHealth)), 0, 100)
        self.currentShape = Shape("Coolship", cExpression)
        self.shoot = False
        self.addTag("Player")
        
        self.weapon = Shotgun(self)
        
        lifeTimeFunc = lambda tA : 2.0
        posFunc = lambda tr, tA: tr.getForward() * (math.sinh(math.pow(tA/lifeTimeFunc(1.0),3)) * 2.5 * Game.unitLength)
        scaleFunc = lambda tA : Vector(0.15, 0.15) * ((lifeTimeFunc(1.0) - tA) / lifeTimeFunc(1.0)) * Game.unitLength
        colorFunc = lambda tA : cExpression()
        
        auraSettings = ParticleSystemEmission(0, 1.0, 180.0, 100.0)
        self.aura = ParticleSystem(screen, self.transform.copy(), posFunc, scaleFunc, lifeTimeFunc, colorFunc, True, auraSettings)
        
    def setShotPointTransform(self):
        posVec = self.transform.position + (self.transform.getForward() * 0.5 * Game.unitLength)
        self.shotPoint = posVec

    def tick(self, deltaTime):
        if self.disposed:
            return
        
        self.aura.tick(deltaTime)
        strobeSpeed = self.maxHealth / (0.05 if self.currentHealth <= 0.0 else self.currentHealth)
        scaleExpression = 1.5 + (math.sin(strobeSpeed * Game.time) * 0.1)
        self.currentShape.drawShape(self.screen, [self.transform.position.x, self.transform.position.y], scaleExpression, self.transform.zAngle - 90)
        self.movement.tick(deltaTime)
        self.rotation.tick()

        self.setShotPointTransform()
        self.weapon.run(deltaTime * 2.0)
        
        return super().tick(deltaTime)
    
    def interact(self, args, type: str):
        if type == "Heal":
            self.currentHealth += args
        elif type == "Damage":
            self.currentHealth -= args
        
        if self.currentHealth <= 0:
            self.dispose()
        
        return super().interact(args, type)
    
from Behaviours.Weapons.Basic import Basic
from Behaviours.Weapons.Shotgun import Shotgun