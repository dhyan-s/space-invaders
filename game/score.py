from typing import Tuple
import pygame

class ScoreHandler:
    def __init__(self, display: pygame.Surface, enemy_img: pygame.Surface):
        self.display = display
        self.enemy_img = enemy_img
        
        self._load_images()
        
        self.__score = 0
        self.__highscore = 0
        self.text_font = pygame.font.Font("assets/fonts/04B_19.TTF", 25)
        
    def _load_images(self):
        img_size = 35
        wh_ratio = self.enemy_img.get_width() / self.enemy_img.get_height()
        h = img_size
        w = h * wh_ratio
        self.enemy_img = pygame.transform.scale(self.enemy_img, (w, h))
        
        overlay = pygame.Surface(self.enemy_img.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 128))
        self.enemy_img.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        
        self.highscore_img = pygame.image.load("assets/images/trophy.png")
        self.highscore_img = pygame.transform.scale(self.highscore_img, (img_size-5, img_size-5))
        
        self.enemy_img_rect = self.enemy_img.get_rect()
        self.highscore_img_rect = self.highscore_img.get_rect()
        
    def render(self):
        display_width, display_height = self.display.get_size()
        self.score_text = self.text_font.render(str(self.__score), True, "white")
        self.highscore_text = self.text_font.render(str(self.__highscore), True, "white")
        
        self.highscore_img_rect.bottomright = (display_width - self.highscore_text.get_width() - 30, display_height - 10)
        self.enemy_img_rect.midbottom = (self.highscore_img_rect.centerx, self.highscore_img_rect.top - 20)
        
        score_rect = self.score_text.get_rect()
        highscore_rect = self.highscore_text.get_rect()
        
        score_rect.midleft = (self.enemy_img_rect.right+10, self.enemy_img_rect.centery)
        highscore_rect.midleft = (score_rect.left, self.highscore_img_rect.centery)
        
        self.display.blit(self.highscore_img, self.highscore_img_rect)
        self.display.blit(self.enemy_img, self.enemy_img_rect)
        
        self.display.blit(self.score_text, score_rect)
        self.display.blit(self.highscore_text, highscore_rect)
        
    def increment_score_by(self, val: int):
        self.set_score_to(self.__score + val)
        
    def set_score_to(self, val: int):
        self.__score = val
        self.check_highscore()
        
    def reset_score(self):
        self.__score = 0
        
    def check_highscore(self):
        if self.__score > self.__highscore:
            self.__highscore = self.__score
            
    def get_score(self) -> int: return self.score
    def get_highscore(self) -> int: return self.highscore