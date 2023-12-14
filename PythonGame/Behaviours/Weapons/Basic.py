from Entities.Projectiles.Bullet import Bullet
from Vector import Vector
from Transform import Transform
from Behaviours.Weapons.Weapon import Weapon
from Entities.Player.Player import Player
import Behaviours.Weapons.WeaponStats as WeaponStats
import Input
import pygame
import Game

class Basic(Weapon):
    def __init__(self, player:Player) -> None:
        self.fireFrequency = 1.0 / WeaponStats.FIRERATE_BASIC
        self.fireDelay = self.fireFrequency
        self.player = player
        super().__init__()
    
    def run(self, deltaTime):
        if Input.getKeyState(pygame.K_SPACE) == False:
            self.fireDelay = self.fireFrequency
            return
        
        if self.fireDelay > 0.0:
            self.fireDelay -= deltaTime * self.clockSpeed
            return
        
        shotPosition = self.player.transform.position + self.player.transform.getForward().normalize() * 25.0
        shotDirection = self.player.transform.getForward().normalize()
        Game.objmngr.InstanceQueue.append(Bullet(Game.screen, Transform(shotPosition, Vector(1.0, 1.0)), shotPosition, shotDirection, WeaponStats.SPEED_BULLET))
        self.fireDelay = self.fireFrequency
        super().run(deltaTime)
    
    def reset():
        super().reset()