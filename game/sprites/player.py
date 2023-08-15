import pygame
import math
from typing import List

from .bar import Bar

class Player:
    def __init__(self, display: pygame.Surface):
        self.display = display
        
        self.__load()
        
        # Player movement
        self.movement_vel = 6.5
        self.nitro_boost = 200
        self.nitro_boost_unit = int(self.nitro_boost / self.nitro_bar.to)
        # Positioning
        self.health_nitro_bar_spacing = 5
        # Bullet
        self.bullet_vel = 10
        self.firing_cooldown = 150
        self.last_fired = 0
        
    def __load(self) -> None:
        # Player
        self.image = pygame.image.load("assets/images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 98))
        self.img_rect = self.image.get_rect()
        
        self.health_bar = Bar(self.display, width=50, height=10, from_=0, to=100, outline_width=1, outline_color="green", value=100)
        self.nitro_bar = Bar(self.display, width=50, height=10, fill_color="gold", from_=0, to=10, outline_width=1, outline_color="gold", value=10)
        
        self.bullet_img = pygame.image.load("assets/images/bullet.png").convert_alpha()
        original_dimensions = self.bullet_img.get_size()
        new_height = 50
        new_width = new_height * (original_dimensions[0] / original_dimensions[1])
        self.bullet_img = pygame.transform.scale(self.bullet_img , (new_width, new_height))
        self.bullet_rects: List[pygame.Rect] = []
        
    def handle_player_movement(self) -> None:
        keys = pygame.key.get_pressed()
        
        # Determine movement velocity
        x_change = 0
        if keys[pygame.K_LEFT]:
            x_change = -self.movement_vel
        elif keys[pygame.K_RIGHT]:
            x_change = self.movement_vel
            
        # Handle nitro
        if keys[pygame.K_RCTRL] and (self.nitro_bar.value > 0 and x_change != 0):
            self.nitro_boost -= 1
            x_change *= 2
            
        # Move player image
        self.img_rect.x += x_change
        self.img_rect.left = max(0, self.img_rect.left)
        self.img_rect.right = min(self.display.get_width(), self.img_rect.right)
        
    def update(self):
        self.handle_player_movement()
        self.handle_bullet_movement()
        self.render_bullets()
        self.display.blit(self.image, self.img_rect)
        self.health_bar.update()
        self.nitro_bar.update()
        self.update_health_bar()
        self.update_nitro_bar()
        
    def update_health_bar(self) -> None:
        self.health_bar.rect.left = self.img_rect.left
        self.health_bar.rect.width = self.img_rect.width * 0.75
        self.health_bar.rect.top = self.img_rect.bottom + 10
        
        if self.health_bar.value < 20:
            self.health_bar.fill_color = "red"
        elif self.health_bar.value < 50:
            self.health_bar.fill_color = "orange"
        else:
            self.health_bar.fill_color = "green"
        self.health_bar.value -= 0.1
        
    def update_nitro_bar(self) -> None:
        self.nitro_bar.value = math.ceil(self.nitro_boost / self.nitro_boost_unit)
        
        self.nitro_bar.rect.right = self.img_rect.right
        self.nitro_bar.rect.width = self.img_rect.width - self.health_bar.rect.width - self.health_nitro_bar_spacing
        self.nitro_bar.rect.top = self.health_bar.rect.top
        
    def fire_bullet(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fired < self.firing_cooldown:
            return
        bullet_rect = self.bullet_img.get_rect()
        bullet_rect.center = self.img_rect.center
        self.bullet_rects.append(bullet_rect)
        self.last_fired = current_time
        
    def handle_bullet_movement(self) -> None:
        for rect in reversed(self.bullet_rects):
            if rect.bottom < 0:
                self.bullet_rects.remove(rect)
            rect.y -= self.bullet_vel
            
    def render_bullets(self) -> None:
        for rect in self.bullet_rects:
            self.display.blit(self.bullet_img, rect)