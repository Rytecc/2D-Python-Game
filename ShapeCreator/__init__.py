import pygame
import numpy
import math
canvasSize = numpy.array([500, 500])

pygame.init()
screen = pygame.display.set_mode(canvasSize)
clock = pygame.time.Clock()
running = True
points = []

def roundToScreenTenth(x) -> float:
    x /= canvasSize[0] * 0.1
    return round(x) * (canvasSize[0] * 0.1)

def generatePoint(screenPos:numpy.array):
    screenPos[0] = roundToScreenTenth(screenPos[0])
    screenPos[1] = roundToScreenTenth(screenPos[1])
    points.append(pygame.Vector2(screenPos[0], screenPos[1]))

def saveCoordinatesFromCenter():
    saveFile = open("newShape.shape", "w")
    for p in points:
        center = canvasSize * 0.5
        relPos = (center - p) / canvasSize
        coordLine = f"{relPos[0]},{relPos[1]}\n"
        saveFile.write(coordLine)

    saveFile.close()

pygame.display.set_caption("Polygon Creator")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                generatePoint(numpy.array(pygame.mouse.get_pos()) * 1.0)
            if pygame.mouse.get_pressed()[2]:
                if points.__len__() > 0: del points[-1]
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_s]: 
                saveCoordinatesFromCenter()
            elif pygame.key.get_pressed()[pygame.K_c]:
                points.clear()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    #Draw an ellipse so the user knows where they are making a point
    mousePos = pygame.mouse.get_pos()
    pointRadius = 3
    pygame.draw.ellipse(screen, "red", [roundToScreenTenth(mousePos[0]) - pointRadius, roundToScreenTenth(mousePos[1]) - pointRadius, pointRadius * 2, pointRadius * 2])
    pygame.draw.ellipse(screen, "green", [canvasSize[0] / 2.0, canvasSize[1] / 2.0, 1, 1])

    # Draw All Stored Lines
    for x in range(0, points.__len__() - 1):
        pygame.draw.aaline(screen, "white", points[x], points[x + 1])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()