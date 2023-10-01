import pygame

from .sprites.player import Player
from .sprites.enemy import Enemy

class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        
        self._load_game_objects()
        
    def _load_game_objects(self):
        self.background = pygame.image.load("assets/images/background.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.display.get_width(), self.display.get_height()))
        self.background.set_alpha(200)
        
        self.player = Player(self.display)
        self.player.rect.midbottom = (self.display.get_width() / 2, self.display.get_height() - 50)
        
        self.event = pygame.USEREVENT
        pygame.time.set_timer(self.event, 800)
        self.enemy = Enemy(self.display)
        self.enemy.rect.center = (100, 100)
        
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.fire_bullet()
        if event.type == self.event:
            self.enemy.fire_bullets(slots=[1])
        
        
    def update(self) -> None:
        self.display.blit(self.background, (0, 0))
        self.player.update()
        self.enemy.update()