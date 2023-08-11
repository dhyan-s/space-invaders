import pygame

class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        
        self.background = pygame.image.load("assets/images/background.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.display.get_width(), self.display.get_height()))
        
    def render(self) -> None:
        self.display.blit(self.background, (0, 0))