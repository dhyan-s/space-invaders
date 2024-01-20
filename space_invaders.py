import pygame
import sys

from game import Game, GameStateManager, GameOver

pygame.init()
pygame.mixer.init()

SCREENWIDTH = 1100
SCREENHEIGHT = 800
FPS = 120

display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Space Invaders by Dhyanesh!")

background = pygame.image.load("assets/images/background.jpg").convert_alpha()
background = pygame.transform.scale(background, (display.get_width(), display.get_height()))
background.set_alpha(200)

game_state_manager = GameStateManager()

game = Game(display, game_state_manager)
game_over = GameOver(display, game_state_manager)

game_state_manager.add_state('game', game)
game_state_manager.add_state('game_over', game_over)
game_state_manager.set_current_state('game')


while True:
    display.fill((0, 0, 0))
    display.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save_game_data()
            pygame.quit() 
            sys.exit()
        game_state_manager.handle_event(event)
            
    game_state_manager.render()
            
    pygame.display.update()
    clock.tick(FPS)