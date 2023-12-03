import pygame

def getHorizontal() -> float:
    keyStates = pygame.key.get_pressed()
    return -1.0 if keyStates[pygame.K_a] else 1.0 if keyStates[pygame.K_d] else 0.0

def getVertical() -> float:
    keyStates = pygame.key.get_pressed()
    return -1.0 if keyStates[pygame.K_s] else 1.0 if keyStates[pygame.K_w] else 0.0

def getKeyState(keyID):
    return pygame.key.get_pressed()[keyID]