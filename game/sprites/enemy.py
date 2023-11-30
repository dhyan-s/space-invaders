import pygame
from typing import List, Tuple, Union
import random

from .bullet import Bullet
from .bar import Bar
from .character import Character

class Slots:
    def __init__(self, 
                 sprite_rect: pygame.Rect,
                 slot_factors: List[Tuple[float, float]] = None) -> None:
        self.factors = slot_factors if slot_factors is not None else []
        self.rect = sprite_rect
        
    def add(self, factor: Tuple[float, float]) -> None:
        self.factors.append((factor, 0))
        
    def remove(self, factor: Tuple[float, float]) -> None:
        self.factors.remove(factor)
        
    @property
    def no_of_slots(self) -> int:
        return len(self.factors)
        
    def get_slot_coords(self, slot_idx: int):
        slot_factors = self.factors[slot_idx]
        return (self.rect.left + self.rect.width * slot_factors[0], self.rect.top + self.rect.height * slot_factors[1])


class AutoFire:
    def __init__(self, 
                 autofire: bool,
                 delay_range: Tuple[int, int],
                 no_of_slots: int,
                 max_fireable_slots: int,
                 disabled_slots: List[int] = None,
                 initial_delay_range: Tuple[int, int] = None) -> None:
        self.autofire = autofire
        self.delay_range = delay_range
        self.no_of_slots = no_of_slots
        self.max_fireable_slots = max_fireable_slots
        self.disabled_slots = disabled_slots if disabled_slots is not None else []
        
        self.last_fire_time = pygame.time.get_ticks()
        self.delay = random.randint(*(initial_delay_range if initial_delay_range is not None else delay_range))
        
    def get_rand_firing_slots(self) -> List[int]:
        slots = [slot for slot in range(self.no_of_slots) if slot not in self.disabled_slots]
        slots_to_fire = random.randint(0, min(self.max_fireable_slots, len(slots)))
        return random.sample(slots, slots_to_fire)
    
    def ready_to_fire(self) -> bool:
        return self.autofire and pygame.time.get_ticks() - self.last_fire_time >= self.delay
    
    def update_firing_attributes(self) -> None:
        self.last_fire_time = pygame.time.get_ticks()
        self.delay = random.randint(*self.delay_range)
        


class Enemy(Character): # TODO: Clean up 
    def __init__(self) -> None:
        self.__load()
        
        self.bullet_vel = 2
        self.show_health_bar = False
        
    def __load(self) -> None:
        self.image = pygame.image.load("assets/images/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (100 , 75))
        
        self.bullet_img = pygame.image.load("assets/images/enemy_bullet.png").convert_alpha()
        self.bullet_img = pygame.transform.rotate(self.bullet_img, 180)
        self.bullet_img = pygame.transform.scale(self.bullet_img , (40, 40))
        
        super().__init__(self.image, self.bullet_img)
        
        self.slots = Slots(
            sprite_rect=self.rect,
            slot_factors=[(0.22, 0.5), (0.5, 0.5), (0.78, 0.5)]
        )
        
        self.autofire = AutoFire(
            autofire=False,
            delay_range=(2000, 5000),
            no_of_slots=self.slots.no_of_slots,
            max_fireable_slots=self.slots.no_of_slots,
            initial_delay_range=(500, 2000),
        )
        
        self.health_bar = Bar(
            from_=0,
            value=self.durability,
            to=self.durability,
            width=70,
            height=7,
            colors=[
                [50, "orange", "black"],
                [20, "red", "black"]
            ]
        )
        
    def is_useless(self) -> None:
        return self.health <= 0 and len(self.bullets.sprites()) == 0
    
    def update_health_bar(self) -> None:
        self.health_bar.rect.centerx = self.rect.centerx
        self.health_bar.rect.y = self.rect.bottom + 10

    def __fire_bullet(self, slot: int = 0) -> None:
        if slot > self.slots.no_of_slots - 1:
            raise ValueError('Slot index out of range.')
        bullet = Bullet(self.bullet_img, self.bullet_vel)
        bullet.rect.midtop = self.slots.get_slot_coords(slot)
        bullet.fire()
        bullet.damage = 30
        self.bullets.add(bullet)
        
    def fire_bullet(self, slots: Union[List[int], int] = 1) -> None:
        slots = [slots] if isinstance(slots, int) else slots
        for slot in list(set(slots)): 
            self.__fire_bullet(slot)
            
    def handle_auto_fire(self) -> None:
        if self.autofire.ready_to_fire():
            self.fire_bullet(self.autofire.get_rand_firing_slots())
            self.autofire.update_firing_attributes()
            
    def update(self, surface: pygame.Surface) -> None:
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.rect.top >= surface.get_height():
                bullet.kill()
        self.handle_auto_fire()
        self.update_health_bar()
    
    def draw(self, surface: pygame.Surface):
        self.bullets.draw(surface)
        if self.show_health_bar:
            self.health_bar.draw(surface)
        surface.blit(self.image, self.rect)
            