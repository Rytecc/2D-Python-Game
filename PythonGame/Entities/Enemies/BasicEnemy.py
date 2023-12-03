from Transform import Transform
from TickedObject import TickedObject
from Vector import Vector
from Shapes.Shape import Shape
from pygame.color import Color
import Game
import math

class BasicEnemy(TickedObject):
    def __init__(self, screen, target:TickedObject, Transform: Transform):
        self.angularVelocity = 0.0
        self.target = target
        self.maxHealth = 10.0
        self.currentHealth = self.maxHealth
        self.healthFrac = lambda:(self.currentHealth / self.maxHealth)
        cExpression = lambda:Color(int(255.0 * self.healthFrac()), int(255.0 * (1.0 - self.healthFrac())), 0)
        self.shape = Shape("Ship", cExpression)
        self.screen = screen
        self.angle = 0
        self.spawnTime = Game.time
        super().__init__(screen, Transform)

    def tick(self, deltaTime):
        if self.currentHealth <= 0.0:
            self.dispose()
            return

        if self.disposed:
            return
        
        selfPos = self.transform.position
        targetPos = self.target.transform.position

        self.angularVelocity = self.transform.getForward().normalize().crossProduct((targetPos - selfPos).normalize()) * 25.0
        self.shape.drawShape(self.screen, [self.transform.position.x, self.transform.position.y], math.pow(math.sin((Game.time - self.spawnTime) * 10.0) * 0.1 + 1.0, 2.0), self.transform.zAngle - 90)
        self.transform.zAngle += self.angularVelocity

        self.transform.Translate(self.transform.getForward().normalize() * (Game.unitLength * 0.01 * deltaTime))
        return super().tick(deltaTime)
    
    def interact(self, args, type:str):
        if type == "Damage":
            self.currentHealth -= args
        
        return super().interact(args, type)