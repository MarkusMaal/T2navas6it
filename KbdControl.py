import sys
from random import *


def KeyControl(pygame, player, speed, dead):
    if player.dead:
        pass
    if player.keys[0] == False:
        if speed > 0:
            speed -= 0.17
            player.traction += 0.6 * 0.034
        elif speed < 0:
            speed = 0
            player.traction = 6
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:          
            if not dead:
                if event.key == pygame.K_LEFT:
                    player.keys[1] = True
                if event.key == pygame.K_UP:
                    speed += 0.25
                    player.keys[0] = True
                if event.key == pygame.K_RIGHT:
                    player.keys[3] = True
                if event.key == pygame.K_DOWN:
                    speed -= 0.25
                    player.keys[2] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.keys[1] = False
            if event.key == pygame.K_UP:
                player.keys[0] = False
            if event.key == pygame.K_DOWN:
                player.keys[2] = False
            if event.key == pygame.K_RIGHT:
                player.keys[3] = False
    if player.keys[0] == True:
        if speed < 45:
            speed += 0.25
            player.traction -= 0.6 * 0.05
        return speed
    if player.keys[2] == True:
        speed -= 1
        player.traction += 0.6 * 0.05
        return speed
    return speed
