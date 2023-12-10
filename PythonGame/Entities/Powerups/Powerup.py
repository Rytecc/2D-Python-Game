from Entities.Player.Player import Player

class Buff:
    def __init__(self, lifeTime) -> None:
        self.lifeTime = lifeTime
        self.alive = True
        pass
    
    def apply(self, target:Player, deltaTime):
        if self.lifeTime < 0.0:
            self.alive = False
            self.unApply(target)
            return

        self.lifeTime -= deltaTime
        
    def unApply(self, target:Player):
        pass