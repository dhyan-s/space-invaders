import pygame

from .bar import Bar
from .character import Character

class Player(Character):
    def __init__(self) -> None:
        self.__load()
        
        self.health_nitro_bar_spacing = 5
        self.firing_cooldown = 120
        
    def __load(self) -> None:
        self.image = pygame.image.load("assets/images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 98))
        
        self.bullet_img = pygame.image.load("assets/images/bullet.png").convert_alpha()
        self.bullet_img = pygame.transform.scale(self.bullet_img , (40, 40))
        
        super().__init__(self.image, self.bullet_img)
        
        self.health_bar.width = 50
        self.health_bar.height = 10
        
        self.nitro_bar = Bar(width=50, height=10, 
                             from_=0, to=10, 
                             outline_width=1, outline_color="gold", 
                             value=10, fill_color="gold")
        
    def handle_movement(self, surface: pygame.Surface) -> None:
        keys = pygame.key.get_pressed()
        # Determine movement velocity
        x_change = 0
        if keys[pygame.K_LEFT]:
            x_change = -self.vel
        if keys[pygame.K_RIGHT]:
            x_change = self.vel
        # Handle nitro
        if keys[pygame.K_RCTRL] and self.nitro_bar.value > 0 and x_change != 0:
            self.nitro_bar.value -= 0.04
            x_change *= 2
        # Move player image
        self.rect.x += x_change
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(surface.get_width(), self.rect.right)
        
    def update_health_bar(self) -> None:
        self.health_bar.rect.left = self.rect.left
        self.health_bar.width = self.rect.width * 0.75
        self.health_bar.rect.top = self.rect.bottom + 10
        
    def update_nitro_bar(self) -> None:
        self.nitro_bar.rect.right = self.rect.right
        self.nitro_bar.width = self.rect.width - self.health_bar.width - self.health_nitro_bar_spacing
        self.nitro_bar.rect.top = self.health_bar.rect.top
        
    def update(self, surface: pygame.Surface):
        self.handle_movement(surface)
        self.bullets.update()
        self.update_health_bar()
        self.update_nitro_bar()
        
    def draw(self, surface: pygame.Surface):
        self.bullets.draw(surface)
        self.health_bar.draw(surface)
        self.nitro_bar.draw(surface)
        surface.blit(self.image, self.rect)
