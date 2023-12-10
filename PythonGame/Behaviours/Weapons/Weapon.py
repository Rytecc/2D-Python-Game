import abc

class Weapon:
    @abc.abstractmethod
    def __init__(self) -> None:
        self.clockSpeed = 1.0
        pass
    
    @abc.abstractmethod
    def run(self, deltaTime):
        pass
    
    @abc.abstractmethod
    def reset(self):
        pass