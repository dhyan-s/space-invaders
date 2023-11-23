import pygame
from typing import Union, Tuple

class Bar:
    def __init__(self, 
                 fill_color: Union[str, Tuple[int, int, int]] = "green",
                 empty_color: Union[str, Tuple[int, int, int]] = "black",
                 width: int = 100,
                 height: int = 20,
                 orient: str = "h",
                 flipped: bool = False,
                 from_: int = 0,
                 to: int = 100,
                 value: int = 30,
                 outline_width: int = 0,
                 outline_color: Union[str, Tuple[int, int, int]] = "red"):
        self.fill_color = fill_color
        self.empty_color = empty_color
        self.from_ = from_
        self.to = to
        self.value = max(value, self.from_)
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.orient = orient
        self.flipped = flipped
        
        self.rect = pygame.Rect(0, 0, width, height)
        
    def render_outline(self, surface: pygame.Surface) -> None:
        if self.outline_width > 0:
            pygame.draw.rect(surface, self.outline_color, self.rect, self.outline_width)
            
    def render_horiontal(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.empty_color, self.rect)
        fill_width = min(self.rect.width * ((self.value - self.from_) / self.to), self.rect.width)
        pygame.draw.rect(surface, self.fill_color, (self.rect.right - fill_width if self.flipped else self.rect.x, self.rect.y, fill_width, self.rect.height))
        self.render_outline(surface)
        
    def render_vertical(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.empty_color, self.rect)
        fill_height = min(self.rect.height * ((self.value - self.from_) / self.to), self.rect.height)
        pygame.draw.rect(surface, self.fill_color, (self.rect.x, self.rect.y if self.flipped else (self.rect.bottom - fill_height), self.rect.width, fill_height))
        self.render_outline(surface)
    
    def flip_dimensions(self) -> None:
        self.width, self.height = self.height, self.width
    
    def draw(self, surface: pygame.Surface) -> None:
        if self.orient.lower() in ["h", "horizontal"]:
            self.render_horiontal(surface)
        elif self.orient.lower() in ["v", "vertical"]:
            self.render_vertical(surface)
        else:
            raise ValueError(f"Invalid orient {self.orient}. Must be 'h' or 'v'.")
        