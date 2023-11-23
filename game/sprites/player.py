import pygame
import math
from typing import List, Union

from .bar import Bar
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        # Player and movement
        self.__durability = 100
        self.movement_vel = 6.5
        self.nitro_boost = 200
        # Positioning
        self.health_nitro_bar_spacing = 5
        # Bullet
        self.bullet_vel = 10
        self.firing_cooldown = 150
        self.last_fired = 0
        
        self.__load()
        
        self.nitro_boost_unit = int(self.nitro_boost / self.nitro_bar.to)
        
    def __load(self) -> None:
        # Player
        self.image = pygame.image.load("assets/images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 98))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.health_bar = Bar(width=50, height=10, from_=0, to=self.durability, outline_width=1, outline_color="green", value=self.durability)
        self.nitro_bar = Bar(width=50, height=10, fill_color="gold", from_=0, to=10, outline_width=1, outline_color="gold", value=10)
        
        self.bullet_img = pygame.image.load("assets/images/bullet.png").convert_alpha()
        self.bullet_img = pygame.transform.scale(self.bullet_img , (40, 40))
        self.bullets = pygame.sprite.Group()
        
    @property
    def durability(self) -> int:
        return self.__durability
    
    @durability.setter
    def durability(self, val: int) -> None:
        self.health_bar.to = val
        self.__durability = val
        
    @property
    def health(self) -> Union[int, float]:
        return self.health_bar.value
    
    @health.setter
    def health(self, new_health: Union[int, float]):
        self.health_bar.value = new_health
        
    def handle_player_movement(self, surface: pygame.Surface) -> None:
        keys = pygame.key.get_pressed()
        # Determine movement velocity
        x_change = 0
        if keys[pygame.K_LEFT]:
            x_change = -self.movement_vel
        if keys[pygame.K_RIGHT]:
            x_change = self.movement_vel
        # Handle nitro
        if keys[pygame.K_RCTRL] and self.nitro_bar.value > 0 and x_change != 0:
            self.nitro_boost -= 1
            x_change *= 2
        # Move player image
        self.rect.x += x_change
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(surface.get_width(), self.rect.right)
        
    def update(self, surface: pygame.Surface):
        self.handle_player_movement(surface)
        self.bullets.update()
        self.update_health_bar()
        self.update_nitro_bar()
        
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)
        self.health_bar.draw(surface)
        self.nitro_bar.draw(surface)
        
    def update_health_bar(self) -> None:
        self.health_bar.rect.left = self.rect.left
        self.health_bar.rect.width = self.rect.width * 0.75
        self.health_bar.rect.top = self.rect.bottom + 10
        
        if self.health_bar.value < 20:
            self.health_bar.fill_color = "red"
            self.health_bar.outline_color = "red"
        elif self.health_bar.value < 50:
            self.health_bar.fill_color = "orange"
            self.health_bar.outline_color = "orange"
        else:
            self.health_bar.fill_color = "green"
            self.health_bar.outline_color = "green"
        # self.health_bar.value -= 0.1
        
    def update_nitro_bar(self) -> None:
        self.nitro_bar.value = math.ceil(self.nitro_boost / self.nitro_boost_unit)
        
        self.nitro_bar.rect.right = self.rect.right
        self.nitro_bar.rect.width = self.rect.width - self.health_bar.rect.width - self.health_nitro_bar_spacing
        self.nitro_bar.rect.top = self.health_bar.rect.top
        
    def fire_bullet(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fired < self.firing_cooldown:
            return
        bullet = Bullet(self.bullet_img, -self.bullet_vel)
        bullet.rect.center = self.rect.center
        bullet.fire()
        self.bullets.add(bullet)
        self.last_fired = current_time
