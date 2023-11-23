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
        
        self.enemies = pygame.sprite.Group()
        self._deleted_enemies: List[Enemy] = []
        
    def spawn_enemy(self) -> None:
        section_width = self.display.get_width() / self.no_sections
        spawn_section = random.randint(0, self.no_sections)
        spawn_point = spawn_section*section_width + section_width / 2
        
        enemy = Enemy()
        enemy.rect.centerx = spawn_point
        enemy.rect.bottom = 0
        
        enemy.bullet_vel = self.enemy_bullet_vel
        enemy.durability = random.choice(self.durability_probs)
        enemy.health_bar.value = enemy.durability
        enemy.autofire.autofire = True
        enemy.autofire.delay_range = (3000, 8000)
        
        self.enemies.add(enemy)
        
    def handle_spawning(self) -> None:
        if len(self.enemies) >= self.max_enemies or pygame.time.get_ticks() - self.__last_spawn_time < self.__delay:
            return
        max_slots = self.max_enemies - len(self.enemies)
        no_of_enemies = random.randint(
            min(max_slots, self.enemy_spawn_range[0]),
            min(max_slots, self.enemy_spawn_range[1]),
        )
        for _ in range(no_of_enemies):
            self.spawn_enemy()
        self.__delay = random.randint(*self.delay_range)
        self.__last_spawn_time = pygame.time.get_ticks()
        
    def move_enemies(self) -> None:
        for enemy in self.enemies:
            enemy.rect.y += self.enemy_vel
            
    def delete_enemy(self, enemy: Enemy) -> None:
        assert enemy in self.enemies
        enemy.kill()
        
    def remove_useless_enemies(self) -> None:
        for enemy in self.enemies:
            if enemy.rect.top > self.display.get_height() or enemy.is_useless():
                enemy.kill()
        
    def draw(self) -> None:
        self.handle_spawning()
        self.move_enemies()
        for enemy in self.enemies:
            enemy.show_health_bar = enemy.health < enemy.durability
            enemy.update(self.display)
            if enemy.health > 0:
                enemy.draw(self.display)
            else:
                enemy.bullets.draw(self.display)
        self.remove_useless_enemies()