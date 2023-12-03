from Transform import Transform
from TickedObject import TickedObject
from Entities.Enemies.BasicEnemy import BasicEnemy
from Vector import Vector
import Game
import random
class EnemySpawner(TickedObject):
    def __init__(self, screen, Transform:Transform, spawnRate:float):
        self.maxDelay = 1.0 / spawnRate
        self.currentDelay = self.maxDelay
        super().__init__(screen, Transform)

    def tick(self, deltaTime):
        self.currentDelay -= deltaTime

        if self.currentDelay > 0.0:
            return
        
        spawnPosition = Vector(random.randint(0, 500), random.randint(0, 500))
        newEnemy = BasicEnemy(self.screen, Game.plr, Transform(spawnPosition, Vector(1, 1)))
        newEnemy.addTag("Enemy")

        Game.objmngr.InstanceQueue.append(newEnemy)
        self.currentDelay = self.maxDelay
        return super().tick(deltaTime)