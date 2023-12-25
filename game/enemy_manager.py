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
        self.count = 1
        
        self.spawn_enemies = True        
        self.__last_spawn_time = 0
        self.__delay: int = 0
        
        self.enemies = pygame.sprite.Group()
        self._deleted_enemies: List[Enemy] = []
        
        self.debug = False
        
    def spawn_enemy(self, section: int = None) -> Enemy:
        section_width = self.display.get_width() / self.no_sections
        section = section if section is not None else random.randint(0, self.no_sections - 1)
        spawn_point = section*section_width + section_width / 2
        
        enemy = Enemy()
        enemy.rect.centerx = spawn_point
        enemy.rect.bottom = 0
        
        enemy.label_text = str(self.count)
        self.count += 1
        
        enemy.bullet_vel = self.enemy_bullet_vel
        enemy.durability = random.choice(self.durability_probs)
        enemy.health = enemy.durability
        if self.debug:
            enemy.display_label = True
            print(f"Enemy {enemy.label_text}:\n\t Section: {section}\n\tCenter: {enemy.rect.center}")
        enemy.autofire.autofire = True
        enemy.autofire.delay_range = (3000, 8000)
        
        self.enemies.add(enemy)
        return enemy
        
    def handle_spawning(self) -> None:
        if len(self.enemies) >= self.max_enemies or pygame.time.get_ticks() - self.__last_spawn_time < self.__delay or not self.spawn_enemies:
            return
        max_slots = self.max_enemies - len(self.enemies)
        no_of_enemies = random.randint(
            min(max_slots, self.enemy_spawn_range[0]),
            min(max_slots, self.enemy_spawn_range[1]),
        )
        spawnable_sections = list(range(self.no_sections))
        for _ in range(no_of_enemies):
            section = random.choice(spawnable_sections)
            spawnable_sections.remove(section)
            self.spawn_enemy(section)
        self.__delay = random.randint(*self.delay_range)
        self.__last_spawn_time = pygame.time.get_ticks()
        
    @property
    def debug(self) -> bool:
        return self.__debug
    
    @debug.setter
    def debug(self, value: bool) -> None:
        for enemy in self.enemies:
            enemy.display_label = value
        self.__debug = value
        
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
            if int(enemy.health) > 0:
                enemy.draw(self.display)
            else:
                enemy.bullets.draw(self.display)
        self.remove_useless_enemies()