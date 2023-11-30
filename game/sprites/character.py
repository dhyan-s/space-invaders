import pygame
from .bar import Bar
from .bullet import Bullet
from typing import Union

class Character(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, bullet_image: pygame.Surface) -> None:
        super().__init__()
        
        self.__durability = 100
        self.show_health_bar = True
        
        self.vel = 5
        self.bullet_vel = 10
        self.bullet_damage = 60
        self.firing_cooldown = 0
        self.last_fired = 0
        
        self.image = image
        self.bullet_img = bullet_image
        
        self.__load()
        
    def __load(self) -> None:
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.health_bar = Bar(from_=0, 
                              to=self.durability, 
                              value=self.durability, 
                              fill_color="green",
                              outline_color="green",
                              outline_width=1,
                              colors=[
                                  [50, "orange", "orange"],
                                  [20, "red", "red"]
                              ])
        
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
        
    def fire_bullet(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fired < self.firing_cooldown:
            return
        bullet = Bullet(self.bullet_img, -self.bullet_vel)
        bullet.rect.center = self.rect.center
        bullet.fire()
        bullet.damage = self.bullet_damage
        self.bullets.add(bullet)
        self.last_fired = current_time
        
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)
        if self.show_health_bar:
            self.health_bar.draw(surface)
        