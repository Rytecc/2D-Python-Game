import Entities.Powerups.Powerup as Powerup
from Entities.Player.Player import Player

class FireRateBuff(Powerup.Buff):
    def __init__(self, lifeTime) -> None:
        super().__init__(lifeTime)
        
    def apply(self, target:Player, deltaTime:float):
        target.weapon.clockSpeed = 2.0
        super().apply(target, deltaTime)
        
    def unApply(self, target: Player):
        target.weapon.clockSpeed = 1.0
        super().unApply(target)