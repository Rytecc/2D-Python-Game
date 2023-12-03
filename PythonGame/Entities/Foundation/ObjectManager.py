from TickedObject import TickedObject
from Transform import Transform
import Game

class ObjectManager(TickedObject):
    def __init__(self, screen, Transform: Transform):
        self.InstanceQueue:list[TickedObject] = []
        self.disposeQueue:list[TickedObject] = []
        super().__init__(screen, Transform)

    def tick(self, deltaTime):
        stackLength = self.InstanceQueue.__len__()
        for x in range(0, stackLength):
            Game.InstantiateObject(self.InstanceQueue.pop())

        disposeLength = self.disposeQueue.__len__()
        for x in range(0,disposeLength):
            Game.DestroyObject(self.disposeQueue.pop())
        
        return super().tick(deltaTime)
    
    def dispose(self):
        return super().dispose()