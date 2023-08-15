import pygame
from .sprites.player import Player

class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        
        self._load_game_objects()
        
    def _load_game_objects(self):
        self.background = pygame.image.load("assets/images/background.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.display.get_width(), self.display.get_height()))
        self.background.set_alpha(200)
        
        self.player = Player(self.display)
        self.player.img_rect.midbottom = (self.display.get_width() / 2, self.display.get_height() - 50)
        
    def handle_event(self, event: pygame.event.Event) -> None:
        pass
        
    def update(self) -> None:
        self.display.blit(self.background, (0, 0))
        self.player.update()