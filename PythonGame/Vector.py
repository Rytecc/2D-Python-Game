import math

class Vector:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def magnitude(self) -> float:
        return math.sqrt((self.x * self.x) + (self.y * self.y))
    
    def dotProduct(self, a, b) -> float:
        return a.x * b.x + a.y + b.y
    
    def crossProduct(self, other) -> float:
        return self.x * other.y - self.y * other.x

    def __mul__(self, other:float):
        return Vector(self.x * other, self.y * other)

    def __div__(self, other:float):
        return Vector(self.x / other, self.y / other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f"({self.x},{self.y})"
    
    def normalize(self):
        return self.__div__(self.magnitude())

    def toArray(self) -> list[float]:
        return [self.x, self.y]
    
    def createUnitWIthAngle(self, angle):
        return Vector(math.cos(angle), math.sin(angle))