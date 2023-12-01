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
        
        self.player = Player()
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
        for enemy in self.enemy_manager.enemies:
            for bullet in reversed(self.player.bullets.sprites()):
                if pygame.sprite.collide_mask(bullet, enemy) and enemy.health > 0:
                    enemy.health -= bullet.damage
                    if enemy.health <= 0:
                        self.player.nitro_bar.value += 0.25
                    bullet.kill()
            for bullet in reversed(enemy.bullets.sprites()):
                if pygame.sprite.collide_mask(bullet, self.player):
                    self.player.health -= bullet.damage
                    bullet.kill()
        
    def update(self) -> None:
        self.display.blit(self.background, (0, 0))
        self.check_bullets()
        self.enemy_manager.draw()
        self.player.update(self.display)
        self.player.draw(self.display)