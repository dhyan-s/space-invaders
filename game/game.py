import pygame
from typing import List

from .sprites.player import Player
from .sprites.enemy import Enemy
from .enemy_manager import EnemyManager

class Game:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        
        self._load_game_objects()
        
    def _load_game_objects(self):
        self.background = pygame.image.load("assets/images/background.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.display.get_width(), self.display.get_height()))
        self.background.set_alpha(200)
        
        self.player = Player(self.display)
        self.player.rect.midbottom = (self.display.get_width() / 2, self.display.get_height() - 50)
        self.player.durability = 400
        self.player.health = self.player.durability
        
        self.enemy_manager = EnemyManager(self.display)
        self.enemy_manager.durability_probs = list(range(30, 50))*3 + list(range(60, 90))*2 + list(range(130, 180)) + list(range(180, 240, 5))
        
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.fire_bullet()
        
    def check_bullets(self) -> None:
        for bullet in reversed(self.player.bullet_group.bullet_list):
            for enemy in self.enemy_manager.enemies_list:
                offset = (enemy.rect.x - bullet.rect.x, enemy.rect.y - bullet.rect.y)
                if bullet.mask.overlap(enemy.mask, offset) and enemy.is_alive:
                    enemy.health -= bullet.damage
                    try: self.player.bullet_group.remove(bullet)
                    except ValueError: pass
        for enemy in self.enemy_manager.enemies_list:
            for bullet in reversed(enemy.bullet_group.bullet_list):
                offset = (
                    bullet.rect.x - self.player.rect.x,
                    bullet.rect.y - self.player.rect.y
                )
                if self.player.mask.overlap(bullet.mask, offset):
                    self.player.health -= bullet.damage
                    enemy.bullet_group.bullet_list.remove(bullet)
                
        
    def update(self) -> None:
        self.display.blit(self.background, (0, 0))
        self.check_bullets()
        self.enemy_manager.update_enemies()
        self.player.update()