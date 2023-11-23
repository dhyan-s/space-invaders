import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, 
                 img: pygame.Surface, 
                 vel: int = 5, 
                 damage: int = 60) -> None:
        self.image = img
        self.vel = vel
        self.damage = damage
        
        self.__fired = False
        
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
    def fire(self) -> None:
        self.__fired = True
            
    def update(self) -> None:
        if self.__fired:
            self.rect.y += self.vel
        