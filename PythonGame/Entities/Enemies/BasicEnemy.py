from Transform import Transform
from TickedObject import TickedObject
from Vector import Vector
from Shapes.Shape import Shape
from pygame.color import Color
from Utility import Physics
import Entities.Enemies.EnemyStats as EnemyStats
import Entities.Particles.ParticleSystem as ParticleSystem
import random
import Game
import math

class BasicEnemy(TickedObject):
    def __init__(self, screen, target:TickedObject, Transform: Transform):
        super().__init__(screen, Transform)
        self.angularVelocity = 0.0
        self.target = target
        
        self.maxHealth = EnemyStats.BASIC_ENEMY_HEALTH
        self.currentHealth = self.maxHealth
        self.healthFrac = lambda:(self.currentHealth / self.maxHealth)
        
        cExpression = lambda:Color(int(255.0 * self.healthFrac()), int(255.0 * (1.0 - self.healthFrac())), 0)
        self.shape = Shape("Ship", cExpression)
        
        self.screen = screen
        self.angle = 0
        self.spawnTime = Game.time
        self.addTag("Enemy")
        
        lifeTimeFunction = lambda tA : 1.0
        positionFunction = lambda tr, tA : Vector(0, 0)
        scaleFunction = lambda tA : Vector(1.0, 1.0) * (math.cos(tA / lifeTimeFunction(1.0)) + 1.0) * 0.05 * Game.unitLength
        colorFunction = lambda tA : Color(cExpression().r, cExpression().g, cExpression().b, 127)
        
        emitSettings = ParticleSystem.ParticleSystemEmission(0, 0.25, 45.0, 25.0)
        self.trail = ParticleSystem.ParticleSystem(screen, Transform.copy(), positionFunction, scaleFunction, lifeTimeFunction, colorFunction, False, emitSettings)

    def tick(self, deltaTime):
        if self.currentHealth <= 0.0 or self.target.disposed:
            if random.random() > 0.9:
                Game.spawnPowerUp(self)
            
            self.dispose()
            return

        if self.disposed:
            return
        
        selfPos = self.transform.position
        targetPos = self.target.transform.position
        self.trail.transform = self.transform.copy()
        self.trail.transform.setForward(self.transform.getForward() * -1.0)
        self.trail.tick(deltaTime)
        
        self.angularVelocity = self.transform.getForward().normalize().crossProduct((targetPos - selfPos).normalize()) * 25.0
        self.transform.zAngle += self.angularVelocity
        
        self.transform.Translate(self.transform.getForward().normalize() * (Game.unitLength * EnemyStats.BASIC_ENEMY_SPEED * deltaTime))
        
        scale = 0.5 + math.sin(5.0 * (Game.time - self.spawnTime)) * 0.1
        self.shape.drawShape(self.screen, [self.transform.position.x, self.transform.position.y], scale, self.transform.zAngle - 90)
        
        overlap = Physics.overlapCircle(self.transform.position, Game.unitLength, "Player")
        
        if overlap.__len__() > 0:
            overlap[0].interact(1.0, "Damage")
            self.dispose()
        
        return super().tick(deltaTime)
    
    def interact(self, args, type:str):
        if type == "Damage":
            self.currentHealth -= args
        
        return super().interact(args, type)