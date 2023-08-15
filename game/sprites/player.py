import pygame
import math

from .bar import Bar

class Player:
    def __init__(self, display: pygame.Surface):
        self.display = display
        
        self.vel = 6.5
        self.nitro_boost = 200
        self.__load()
        self.nitro_boost_unit = int(self.nitro_boost / self.nitro_bar.to)
        
        
    def __load(self) -> None:
        self.image = pygame.image.load("assets/images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 98))
        
        self.img_rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        
        self.health_bar = Bar(self.display, width=50, height=8, from_=0, to=100)
        self.nitro_bar = Bar(self.display, width=50, height=7, fill_color="gold", from_=0, to=10, outline_width=1, outline_color="gold")
        self.nitro_bar.value = 10
        self.health_bar.value = 100
        
    def update_nitro_bar(self) -> None:
        self.nitro_bar.value = math.ceil(self.nitro_boost / self.nitro_boost_unit)
        
    def handle_movement(self) -> None:
        keys = pygame.key.get_pressed()
        
        x_change = 0
        if keys[pygame.K_LEFT]:
            x_change = -self.vel
        elif keys[pygame.K_RIGHT]:
            x_change = self.vel
        if keys[pygame.K_RCTRL] and (self.nitro_bar.value > 0 and x_change != 0):
            self.nitro_boost -= 1
            x_change *= 2
            self.update_nitro_bar()
            
        self.img_rect.x += x_change
        self.img_rect.left = max(0, self.img_rect.left)
        self.img_rect.right = min(self.display.get_width(), self.img_rect.right)
        self.health_bar.rect.centerx = self.nitro_bar.rect.centerx = self.img_rect.centerx
        self.health_bar.rect.top = self.img_rect.bottom + 10
        self.nitro_bar.rect.top = self.health_bar.rect.bottom + 10
        
    def update(self):
        self.handle_movement()
        self.display.blit(self.image, self.img_rect)
        self.health_bar.update()
        self.nitro_bar.update()