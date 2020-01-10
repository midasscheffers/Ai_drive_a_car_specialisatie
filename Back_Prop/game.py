import pygame
import math as mth
import random as r
from network import *
from player import *
from wall import *

amount_of_rays = 36
pygame.init()
print(pygame.init())
height = 1080
width = 1920
translationX = width/2
translationY = height/2
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
light_grey = (170, 170, 170)
speed = 3
clock = pygame.time.Clock()
FPS = 60
gameDisplay = pygame.display.set_mode((width, height), pygame.FULLSCREEN) # to make full screen do : , pygame.FULLSCREEN
pygame.display.set_caption("ai game")
pygame.display.update()

players = []
am_of_players = 10

walls = []

walls.append(Wall([-translationX, -translationY], [-translationX, translationY]))
walls.append(Wall([-translationX, translationY-1], [translationX, translationY-1]))
walls.append(Wall([translationX-1, -translationY], [translationX-1, translationY]))
walls.append(Wall([-translationX, -translationY], [translationX, -translationY]))

for i in range(am_of_players):
    players.append(Player([0, 0], amount_of_rays, False))

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            gameExit = True

    
    gameDisplay.fill((200, 200, 200))

    for w in walls:
        w.blit(gameDisplay)

    for p in players:
        p.set_net_input()
        p.move()
        p.cast_rays(walls, gameDisplay)
        p.blit(gameDisplay)

    pygame.display.update()
    # clock.tick(FPS)

pygame.quit()
quit()