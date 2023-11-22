from numpy import disp
import pygame
from typing import List, Tuple, Union, Callable
import random

from .bullet import Bullet, BulletGroup
from .bar import Bar


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
        


class Enemy:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        self.bullet_vel = 2
        self.show_health_bar: bool = False
        self.__durability = 100
        
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
        self.mask = pygame.mask.from_surface(spaceship_image)
        
        self.autofire = AutoFire(
            autofire=False,
            delay_range=(2000, 5000),
            no_of_slots=self.spaceship.no_of_slots,
            max_fireable_slots=self.spaceship.no_of_slots,
            initial_delay_range=(500, 2000),
        )
        
        self.health_bar = Bar(
            display=self.display,
            from_=0,
            value=self.durability,
            to=self.durability,
            width=70,
            height=7,
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
        
    def kill(self) -> None:
        self.health = 0
        
    def revive(self) -> None:
        self.health = self.durability
        
    @property
    def is_alive(self) -> bool:
        return self.health > 0
        
    def is_useless(self) -> None:
        return (not self.is_alive) and self.bullet_group.is_empty()
    
    def update_health_bar(self) -> None:
        self.health_bar.rect.centerx = self.rect.centerx
        self.health_bar.rect.y = self.rect.bottom + 10
        if self.show_health_bar:
            self.health_bar.update()
        
    def update(self) -> None:
        self.bullet_group.update_all()
        if self.is_alive:
            self.handle_auto_fire()
            self.update_health_bar()
            self.spaceship.update(self.display)

    def __fire_bullet(self, slot: int = 0) -> None:
        if slot > self.spaceship.no_of_slots - 1:
            raise ValueError('Slot index out of range.')
            
        bullet = Bullet(self.display, self.bullet_img, self.bullet_vel)
        bullet.rect.midtop = self.spaceship.get_slot_coords(slot)
        bullet.fire()
        self.bullet_group.add(bullet)
        
    def fire_bullets(self, slots: Union[List[int], int] = 1) -> None:
        if not self.is_alive: return
        slots = [slots] if isinstance(slots, int) else slots
        for slot in list(set(slots)): 
            self.__fire_bullet(slot)
            
    def handle_auto_fire(self) -> None:
        if self.autofire.ready_to_fire():
            self.fire_bullets(self.autofire.get_rand_firing_slots())
            self.autofire.update_firing_attributes()
            