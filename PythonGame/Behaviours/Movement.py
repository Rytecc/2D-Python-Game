from Transform import Transform
from Vector import Vector
import Game
import Input

# arg0 = Transform
class Movement:
    def __init__(self, transform:Transform, speed):
        self.transform = transform
        self.speed = speed

    def tick(self, deltaTime):
        moveVec = Vector(Input.getHorizontal(), -Input.getVertical()) * (self.speed * Game.unitLength * deltaTime)
        self.transform.Translate(moveVec * deltaTime)