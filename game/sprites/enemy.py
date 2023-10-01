from outcome import Value
import pygame
from typing import List, Union

class Enemy:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        
        self.__load()
        self.bullet_vel = 2
        
    def __load(self) -> None:
        self.image = pygame.image.load("assets/images/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (100 , 75))
        self.rect = self.image.get_rect()
        
        self.bullet_img = pygame.image.load("assets/images/enemy_bullet.png").convert_alpha()
        self.bullet_img = pygame.transform.rotate(self.bullet_img, 180)
        self.bullet_img = pygame.transform.scale(self.bullet_img , (40, 40))
        self.bullet_rects = []
        
    def update(self) -> None:
        self.handle_bullet_movement()
        self.render_bullets()
        self.display.blit(self.image, self.rect)
        
    def _determine_slot_coordinates(self) -> List[int]:
        slot1_x = self.rect.x + self.rect.width * 0.22
        slot2_x = self.rect.x + self.rect.width * 0.5
        slot3_x = self.rect.x + self.rect.width * 0.78
        return [slot1_x, slot2_x, slot3_x]
        
    def __fire_bullet(self, slot: int = 1) -> None:
        if slot not in [0, 1, 2]:
            raise ValueError(f"Slot must range between 0 and 2, recieved {slot}.")
        slot_coords = self._determine_slot_coordinates()
        bullet_top = self.rect.centery + 10
        bullet_rect = self.bullet_img.get_rect()
        bullet_rect.midtop = (slot_coords[slot], bullet_top)
        self.bullet_rects.append(bullet_rect)
        
    def fire_bullets(self, slots: Union[List[int], int] = 1) -> None:
        slots = [slots] if isinstance(slots, int) else slots
        for slot in list(set(slots)): 
            self.__fire_bullet(slot)
        
    def handle_bullet_movement(self) -> None:
        for rect in reversed(self.bullet_rects):
            if rect.top > self.display.get_height():
                self.bullet_rects.remove(rect)
            rect.y += self.bullet_vel
            
    def render_bullets(self) -> None:
        for rect in self.bullet_rects:
            self.display.blit(self.bullet_img, rect)