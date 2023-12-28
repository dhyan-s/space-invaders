from typing import List
import pygame
from dataclasses import dataclass

from game.game import Game

from .game_state import GameStateManager

@dataclass
class Message:
    text: str
    font: pygame.font.Font
    margin_top: int = 0
    color: pygame.Color = "white"
    
    def render(self) -> pygame.Surface:
        return self.font.render(self.text, True, self.color)

class GameOver:
    def __init__(self, display: pygame.Surface, game_state_manager: GameStateManager):
        self.display = display
        self.game_state_manager = game_state_manager
        
        self.gameover_font = pygame.font.Font("assets/fonts/04B_19.TTF", 110)
        self.message_font = pygame.font.Font("assets/fonts/Inconsolata-Bold.ttf", 40)
        
        self.gameover = Message("GAMEOVER!", self.gameover_font)
        self.continue_ = Message("Press Enter to Continue...", self.message_font, 20)
        self.reason = Message("", self.message_font, 10)
        self.messages = [self.gameover, self.reason, self.continue_]
                
        self.text_surf = pygame.Surface((0, 0), pygame.SRCALPHA, 32)
        
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game: Game = self.game_state_manager.get_state_by_name('game').obj
                game.restart()
                self.game_state_manager.set_current_state('game')
        
    def render_messages(self):
        surf_height = sum(msg.render().get_height() + msg.margin_top for msg in self.messages)
        
        self.text_surf = pygame.transform.scale(self.text_surf, (self.display.get_width(), surf_height))
        self.text_surf.fill((0, 0, 0, 0))
        surf_rect = self.text_surf.get_rect()
        surf_rect.center = self.display.get_rect().center
        
        rendered_msgs: List[pygame.Surface] = [msg.render() for msg in self.messages]
        msg_rects: List[pygame.Rect] = [msg.get_rect() for msg in rendered_msgs]
        for idx, rect in enumerate(msg_rects):
            y = (msg_rects[idx-1].bottom + self.messages[idx].margin_top) if idx > 0 else 0
            rect.midtop = (surf_rect.centerx, y)
        
        for idx, msg in enumerate(rendered_msgs):
            self.text_surf.blit(msg, msg_rects[idx]) 
        self.display.blit(self.text_surf, surf_rect)
        
    def render(self):
        self.render_messages()
        
        