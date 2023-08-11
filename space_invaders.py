import pygame
import sys

from game import Game

pygame.init()

SCREENWIDTH = 1100
SCREENHEIGHT = 800
FPS = 120

display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Space Invaders by Dhyanesh!")

game = Game(display)

while True:
    display.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    game.render()
            
    pygame.display.update()
    clock.tick(FPS)