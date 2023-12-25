import pygame
import time

from .sprites.player import Player
from .enemy_manager import EnemyManager
from .game_state import GameStateManager

class Game:
    def __init__(self, display: pygame.Surface, game_state_manager: GameStateManager) -> None:
        self.display = display
        self.game_state_manager = game_state_manager
        
        self._load_game_objects()
        
    def _load_game_objects(self):
        self.player = Player()
        self.player.rect.midbottom = (self.display.get_width() / 2, self.display.get_height() - 50)
        self.player.durability = 400
        self.player.health = self.player.durability
        
        self.enemy_manager = EnemyManager(self.display)
        self.enemy_manager.durability_probs = list(range(30, 50))*3 + list(range(60, 90))*2 + list(range(130, 180)) + list(range(180, 240, 5))
        self.enemy_manager.debug = True
        
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
                        if self.enemy_manager.debug:
                            print(f"Killed Enemy {enemy.label_text}")
                    bullet.kill()
            for bullet in reversed(enemy.bullets.sprites()):
                if pygame.sprite.collide_mask(bullet, self.player):
                    self.player.health -= bullet.damage
                    bullet.kill()
                    
    def handle_game_over(self) -> None:
        if self.player.health <= 0:
            time.sleep(1)
            self.trigger_game_over("- Player Killed")
            pass
        for enemy in self.enemy_manager.enemies:
            if enemy.rect.centery > self.display.get_height() and enemy.health > 0:
                if self.enemy_manager.debug:
                    print(f"Invaded: {enemy.label_text}")
                time.sleep(1)
                self.trigger_game_over("- Enemy has invaded the planet")
                break
                        
    def trigger_game_over(self, msg: str) -> None:
        self.game_state_manager.set_current_state("game_over")
        reason_msg = self.game_state_manager.get_state_by_name("game_over").obj.reason
        reason_msg.text = msg
        reason_msg.color = "red"
        
    def render(self) -> None:
        self.check_bullets()
        self.enemy_manager.draw()
        self.player.update(self.display)
        self.player.draw(self.display)
        self.handle_game_over()