import abc

class Weapon:
    @abc.abstractmethod
    def __init__(self) -> None:
        pass
    
    @abc.abstractmethod
    def run(self):
        pass
    
    @abc.abstractmethod
    def reset(self):
        pass