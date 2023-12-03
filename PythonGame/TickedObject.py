import abc
from Transform import Transform
import Game
class TickedObject:
    def __init__(self, screen, Transform:Transform):
        self.tags:list[str] = ["default"]
        self.transform = Transform
        self.disposed = False
        self.screen = screen
    
    @abc.abstractmethod
    def tick(self, deltaTime):
        pass

    @abc.abstractmethod
    def dispose(self):
        if self.disposed == True:
            return
        
        Game.objmngr.disposeQueue.append(self)
        self.disposed = True

    def setInstanceID(self, id:int):
        self.instanceID = id

    def addTag(self, tag):
        self.tags.append(tag)

    def interact(self, args, type:str):
        pass