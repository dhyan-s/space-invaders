import pygame
import time
import os
from typing import Dict
import pickle

from .sprites.player import Player
from .sprites.enemy import Enemy
from .enemy_manager import EnemyManager
from .game_state import GameStateManager
from .score import ScoreHandler

class Game:
    def __init__(self, display: pygame.Surface, game_state_manager: GameStateManager) -> None:
        self.display = display
        self.game_state_manager = game_state_manager
        
        self.game_data: Dict = {
            "highscore": 0,
        }
        self.game_data_path = f"{os.path.dirname(__file__)}/game_data.dat"
        
        self.load_sounds()
        self._load_game_objects()
        self.load_game_data()
        
    def _load_game_objects(self):
        self.player = Player()
        self.player.rect.midbottom = (self.display.get_width() / 2, self.display.get_height() - 50)
        self.player.durability = 400
        self.player.health = self.player.durability
        
        self.enemy_manager = EnemyManager(self.display)
        self.enemy_manager.durability_probs = list(range(30, 50))*3 + list(range(60, 90))*2 + list(range(130, 180)) + list(range(180, 240, 5))
        self.enemy_manager.enemy_gunshot_sound = self.sounds['enemy_gunshot']
        # self.enemy_manager.debug = True
        
        self.score = ScoreHandler(self.display, Enemy().image.copy())
        
    def load_game_data(self):
        """
        - Loads the game data from a file and applies it to the game.
        - If the game data file doesn't exist, it creates a new file with default game data.
        - If the file exists but is empty or corrupted, it resets the game data to default values.
        """
        if not os.path.exists(self.game_data_path): # File not found
            self.save_game_data()
        with open(self.game_data_path, "rb") as f:
            try:
                self.game_data = pickle.load(f)
                self.apply_game_data()
            except EOFError as e: # File exists but is likely empty
                self.save_game_data()
            except pickle.UnpicklingError as e: # Corrupted game data
                self.save_game_data()
    
    def save_game_data(self) -> None:
        """Saves the game data to a file."""
        self.game_data["highscore"] = self.score.get_highscore()
        with open(self.game_data_path, "wb") as f:
            pickle.dump(self.game_data, f)
            
    def apply_game_data(self) -> None:
        """Applies the loaded game data to the respective objects in the game."""
        self.score.set_highscore_to(self.game_data['highscore'])
        
    def load_sounds(self):
        self.sounds = {
            'player_damage': 'assets/sounds/player_damage.mp3',
            'player_gunshot': 'assets/sounds/player_gunshot.mp3',
            'enemy_gunshot': 'assets/sounds/enemy_gunshot.mp3',
            'game_over': 'assets/sounds/game_over.mp3',
            'enemy_damage': 'assets/sounds/enemy_damage.mp3'
        }
        self.sounds: Dict[str, pygame.mixer.Sound] = {name: pygame.mixer.Sound(path) for name, path in self.sounds.items()}
        
        self.bg_music_path = 'assets/sounds/bg_music.mp3'
        self.bg_music_full_volume = 0.5
        pygame.mixer.music.load(self.bg_music_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.bg_music_full_volume)
        
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.fire_bullet()
                self.sounds['player_gunshot'].play()
        
    def check_bullets(self) -> None:
        for enemy in self.enemy_manager.enemies:
            for bullet in reversed(self.player.bullets.sprites()):
                if pygame.sprite.collide_mask(bullet, enemy) and enemy.health > 0:
                    enemy.health -= bullet.damage
                    self.sounds['enemy_damage'].play()
                    if enemy.health <= 0:
                        self.player.nitro_bar.value += 0.25
                        self.score.increment_score_by(1)
                        if self.enemy_manager.debug:
                            print(f"Killed Enemy {enemy.label_text}")
                    bullet.kill()
            for bullet in reversed(enemy.bullets.sprites()):
                if pygame.sprite.collide_mask(bullet, self.player):
                    self.player.health -= bullet.damage
                    self.sounds['player_damage'].play()
                    bullet.kill()
                    
    def handle_game_over(self) -> None:
        if self.player.health <= 0:
            self.trigger_game_over("- Player Killed")
        for enemy in self.enemy_manager.enemies:
            if enemy.rect.centery > self.display.get_height() and enemy.health > 0:
                if self.enemy_manager.debug:
                    print(f"Invaded: {enemy.label_text}")
                self.trigger_game_over("- Enemy has invaded the planet")
                break
                        
    def trigger_game_over(self, msg: str) -> None:
        for sound in self.sounds.values():
            sound.stop()
        pygame.mixer.music.set_volume(0.1)
        self.sounds['game_over'].play()
        time.sleep(1.5)
        pygame.mixer.music.set_volume(self.bg_music_full_volume)
        self.game_state_manager.set_current_state("game_over")
        reason_msg = self.game_state_manager.get_state_by_name("game_over").obj.reason
        reason_msg.text = msg
        reason_msg.color = "red"
        
    def restart(self) -> None:
        self.save_game_data()
        self.enemy_manager.enemies.empty()
        self.enemy_manager.count = 1
        self.player.health = self.player.durability
        self.player.nitro = self.player.nitro_bar.to
        self.player.rect.midbottom = (self.display.get_width() / 2, self.display.get_height() - 50)
        self.score.set_score_to(0)
        self.player.bullets.empty()
        
    def render(self) -> None:
        self.check_bullets()
        self.enemy_manager.draw()
        self.player.update(self.display)
        self.player.draw(self.display)
        self.score.render()
        self.handle_game_over()