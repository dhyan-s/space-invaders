import pygame
from typing import List, Tuple, Union
import random
from dataclasses import dataclass, field

from .bullet import Bullet, BulletGroup


class EnemySpaceship:
    def __init__(self, 
                 img: pygame.Surface,
                 slot_factors: List[Tuple[float, float]] = None) -> None:
        self.img = img
        self.slot_factors = slot_factors if slot_factors is not None else []
        self.rect = self.img.get_rect()
        
    @property
    def no_of_slots(self) -> int:
        return len(self.slot_factors)
        
    def get_slot_coords(self, slot_idx: int):
        slot_factors = self.slot_factors[slot_idx]
        return (self.rect.left + self.rect.width * slot_factors[0], self.rect.top + self.rect.height * slot_factors[1])
    
    def update(self, surface: pygame.Surface) -> None:
        surface.blit(self.img, self.rect)


@dataclass
class AutoFire:
    autofire: bool
    delay_range: Tuple[int, int]
    no_of_slots: int
    max_fireable_slots: int
    disabled_slots: List[int] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        self.last_fire_time = 0
        self.delay = 0
        
    def get_rand_firing_slots(self) -> List[int]:
        slots = [slot for slot in range(self.no_of_slots) if slot not in self.disabled_slots]
        slots_to_fire = random.randint(0, min(self.max_fireable_slots, len(slots)))
        return random.sample(slots, slots_to_fire)


class Enemy:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        self.bullet_vel = 2
        
        self.__load()
        
    def __load(self) -> None:
        spaceship_image = pygame.image.load("assets/images/enemy.png").convert_alpha()
        spaceship_image = pygame.transform.scale(spaceship_image , (100 , 75))
        self.spaceship = EnemySpaceship(spaceship_image)
        self.spaceship.slot_factors = [
            (0.22, 0.5),
            (0.5, 0.5),
            (0.78, 0.5)
        ]
        
        self.autofire = AutoFire(
            autofire=False,
            delay_range=(800, 5000),
            no_of_slots=self.spaceship.no_of_slots,
            max_fireable_slots=self.spaceship.no_of_slots
        )
        
        self.bullet_img = pygame.image.load("assets/images/enemy_bullet.png").convert_alpha()
        self.bullet_img = pygame.transform.rotate(self.bullet_img, 180)
        self.bullet_img = pygame.transform.scale(self.bullet_img , (40, 40))
        self.bullet_group = BulletGroup(self.display, lambda bullet: bullet.rect.top > self.display.get_height())
        
    @property
    def rect(self) -> pygame.Rect: 
        return self.spaceship.rect
    
    @rect.setter
    def rect(self, new_rect: pygame.Rect) -> None: 
        self.spaceship.rect = new_rect
        
    def update(self) -> None:
        self.bullet_group.update_all()
        self.handle_auto_fire()
        self.spaceship.update(self.display)

    def __fire_bullet(self, slot: int = 0) -> None:
        if slot > self.spaceship.no_of_slots - 1:
            raise ValueError('Slot index out of range.')
            
        bullet = Bullet(self.display, self.bullet_img, self.bullet_vel)
        bullet.rect.midtop = self.spaceship.get_slot_coords(slot)
        bullet.fire()
        self.bullet_group.add(bullet)
        
    def fire_bullets(self, slots: Union[List[int], int] = 1) -> None:
        slots = [slots] if isinstance(slots, int) else slots
        for slot in list(set(slots)): 
            self.__fire_bullet(slot)
            
    def handle_auto_fire(self) -> None:
        if not self.autofire.autofire or pygame.time.get_ticks() - self.autofire.last_fire_time < self.autofire.delay:
            return
        self.fire_bullets(self.autofire.get_rand_firing_slots())
        self.autofire.last_fire_time = pygame.time.get_ticks()
        self.autofire.delay = random.randint(*self.autofire.delay_range)
            