import pygame
from typing import List, Union

from .bullet import Bullet, BulletGroup

class Enemy:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        self.bullet_vel = 2
        
        self.__load()
        
    def __load(self) -> None:
        self.image = pygame.image.load("assets/images/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (100 , 75))
        self.rect = self.image.get_rect()
        
        self.bullet_img = pygame.image.load("assets/images/enemy_bullet.png").convert_alpha()
        self.bullet_img = pygame.transform.rotate(self.bullet_img, 180)
        self.bullet_img = pygame.transform.scale(self.bullet_img , (40, 40))
        self.bullet_group = BulletGroup(self.display, lambda bullet: bullet.rect.top > self.display.get_height())
        
    def update(self) -> None:
        self.bullet_group.update_all()
        self.display.blit(self.image, self.rect)
        
    def _determine_slot_coordinates(self, slot: int) -> float:
        slot1_x = self.rect.x + self.rect.width * 0.22
        slot2_x = self.rect.x + self.rect.width * 0.5
        slot3_x = self.rect.x + self.rect.width * 0.78
        slot_coordinates = [slot1_x, slot2_x, slot3_x]
        return slot_coordinates[slot]

    def __fire_bullet(self, slot: int = 1) -> None:
        if slot not in [0, 1, 2]:
            raise ValueError(f"Slot must range between 0 and 2, recieved {slot}.")
        bullet = Bullet(self.display, self.bullet_img, self.bullet_vel)
        bullet_top = self.rect.centery + 10
        bullet.rect.midtop = (self._determine_slot_coordinates(slot), bullet_top)
        bullet.fire()
        self.bullet_group.add(bullet)
        
    def fire_bullets(self, slots: Union[List[int], int] = 1) -> None:
        slots = [slots] if isinstance(slots, int) else slots
        for slot in list(set(slots)): 
            self.__fire_bullet(slot)
            