from typing import List, Iterable
import pygame
import random

from .sprites.enemy import Enemy

class EnemyManager:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        
        self.no_sections = 5
        self.enemy_bullet_vel = 2
        self.enemy_vel = 1
        self.enemy_spawn_range = (1,3)
        self.delay_range = (500, 2000)
        self.max_enemies = 7
        self.durability_probs: Iterable[int] = [100]
        
        self.__last_spawn_time = 0
        self.__delay: int = 0
        
        self.enemies_list: List[Enemy] = []
        self._deleted_enemies: List[Enemy] = []
        
    def __iter__(self) -> Iterable[Enemy]:
        return iter(self.enemies_list)
        
    def spawn_enemy(self) -> None:
        section_width = self.display.get_width() / self.no_sections
        spawn_section = random.randint(0, self.no_sections)
        spawn_point = spawn_section*section_width + section_width / 2
        
        enemy = Enemy(self.display)
        enemy.rect.centerx = spawn_point
        enemy.rect.bottom = 0
        
        enemy.bullet_vel = self.enemy_bullet_vel
        enemy.durability = random.choice(self.durability_probs)
        enemy.health_bar.value = enemy.durability
        enemy.autofire.autofire = True
        enemy.autofire.delay_range = (3000, 8000)
        
        self.enemies_list.append(enemy)
        
    def handle_spawning(self) -> None:
        if len(self.enemies_list) >= self.max_enemies or pygame.time.get_ticks() - self.__last_spawn_time < self.__delay:
            return
        max_slots = self.max_enemies - len(self.enemies_list)
        no_of_enemies = random.randint(
            min(max_slots, self.enemy_spawn_range[0]),
            min(max_slots, self.enemy_spawn_range[1]),
        )
        for _ in range(no_of_enemies):
            self.spawn_enemy()
        self.__delay = random.randint(*self.delay_range)
        self.__last_spawn_time = pygame.time.get_ticks()
        
    def move_enemies(self) -> None:
        for enemy in self.enemies_list:
            enemy.rect.y += self.enemy_vel
            
    def delete_enemy(self, enemy: Enemy) -> None:
        assert enemy in self.enemies_list
        enemy.kill()
        
    def remove_useless_enemies(self) -> None:
        for enemy in reversed(self.enemies_list):
            if enemy.rect.top > self.display.get_height() or enemy.is_useless():
                self.enemies_list.remove(enemy)
        
    def update_enemies(self) -> None:
        self.handle_spawning()
        self.move_enemies()
        for enemy in self.enemies_list:
            enemy.show_health_bar = enemy.health < enemy.durability
            enemy.update()
        self.remove_useless_enemies()