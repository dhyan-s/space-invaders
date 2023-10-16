import pygame
from typing import Tuple, List, Callable

class Bullet:
    def __init__(self, display: pygame.Surface, img: pygame.Surface, vel: int = 5, coords: Tuple[int, int] = None) -> None:
        self.display = display
        self.image = img
        self.vel = vel
        
        self.__fired = False
        self.__loaded = False
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0) if coords is None else coords

    def load(self): self.__loaded = True
    def unload(self): self.__loaded = False
        
    def fire(self) -> None:
        self.load()
        self.__fired = True
    
    def handle_movement(self) -> None:
        if self.__fired:
            self.rect.y += self.vel
            
    def update(self) -> None:
        self.handle_movement()
        if self.__loaded:
            self.display.blit(self.image, self.rect)
    

class BulletGroup:
    def __init__(self, display: pygame.Surface, remove_callback: Callable[[Bullet], bool] = None):
        self.display = display
        self.bullet_list: List[Bullet] = []
        self.remove_callback = (lambda b: None) if remove_callback is None else remove_callback
        
    def add(self, bullet: Bullet) -> None:
        self.bullet_list.append(bullet)
        
    def load_all(self) -> None:
        for bullet in self.bullet_list:
            bullet.load()
            
    def unload_all(self) -> None:
        for bullet in self.bullet_list:
            bullet.unload()
            
    def fire_all(self) -> None:
        for bullet in self.bullet_list:
            bullet.fire()
            
    def update_all(self) -> None:
        for bullet in self.bullet_list:
            bullet.update()
            if self.remove_callback(bullet):
                self.bullet_list.remove(bullet)
        