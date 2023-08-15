import pygame
from typing import Union, Tuple

class Bar:
    def __init__(self, 
                 display: pygame.Surface, 
                 fill_color: Union[str, Tuple[int, int, int]] = "green",
                 empty_color: Union[str, Tuple[int, int, int]] = "black",
                 width: int = 100,
                 height: int = 20,
                 from_: int = 0,
                 to: int = 100,
                 value: int = 30,
                 outline_width: int = 0,
                 outline_color: Union[str, Tuple[int, int, int]] = "red"):
        self.display = display
        
        self.fill_color = fill_color
        self.empty_color = empty_color
        self.from_ = from_
        self.to = to
        self.value = max(value, self.from_)
        self.outline_width = outline_width
        self.outline_color = outline_color
        
        self.rect = pygame.Rect(0, 0, width, height)
        
    def update(self):
        pygame.draw.rect(self.display, self.empty_color, self.rect)
        fill_width = min(self.rect.width * ((self.value - self.from_) / self.to), self.rect.width)
        pygame.draw.rect(self.display, self.fill_color, (self.rect.x, self.rect.y, fill_width, self.rect.height))
        if self.outline_width > 0:
            pygame.draw.rect(self.display, self.outline_color, self.rect, self.outline_width)
        
        