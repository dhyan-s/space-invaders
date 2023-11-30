import pygame
from typing import Union, Tuple, List

color = Union[pygame.Color, str, Tuple[int, int, int]]

class Bar:
    def __init__(self, 
                 fill_color: color = "green",
                 empty_color: color = "black",
                 width: int = 100,
                 height: int = 20,
                 orient: str = "h",
                 flipped: bool = False,
                 from_: int = 0,
                 to: int = 100,
                 value: int = 30,
                 outline_width: int = 0,
                 outline_color: color = "red",
                 colors: List[Tuple[int, color, color]] = None):
        self.fill_color = fill_color
        self.empty_color = empty_color
        self.from_ = from_
        self.to = to
        self.value = max(value, self.from_)
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.orient = orient
        self.flipped = flipped
        self.colors = [] if colors is None else colors
        
        self.rect = pygame.Rect(0, 0, width, height)
        
    @property
    def width(self): return self.rect.width
    
    @width.setter
    def width(self, val: int): self.rect.width = val
    
    @property
    def height(self): return self.rect.height
    
    @height.setter
    def height(self, val: int): self.rect.height = val
        
    def render_outline(self, surface: pygame.Surface) -> None:
        outline_color = self.get_colors()[1]
        if self.outline_width > 0:
            pygame.draw.rect(surface, outline_color, self.rect, self.outline_width)
            
    def render_horiontal(self, surface: pygame.Surface) -> None:
        fill_color = self.get_colors()[0]
        pygame.draw.rect(surface, self.empty_color, self.rect)
        fill_width = min(self.width * ((self.value - self.from_) / self.to), self.width)
        pygame.draw.rect(surface, fill_color, (self.rect.right - fill_width if self.flipped else self.rect.x, self.rect.y, fill_width, self.height))
        self.render_outline(surface)
        
    def render_vertical(self, surface: pygame.Surface) -> None:
        fill_color = self.get_colors()[0]
        pygame.draw.rect(surface, self.empty_color, self.rect)
        fill_height = min(self.height * ((self.value - self.from_) / self.to), self.height)
        pygame.draw.rect(surface, fill_color, (self.rect.x, self.rect.y if self.flipped else (self.rect.bottom - fill_height), self.width, fill_height))
        self.render_outline(surface)
    
    def flip_dimensions(self) -> None:
        self.width, self.height = self.height, self.width
        
    def get_colors(self) -> Tuple[color, color]:
        for max_perc, fill_color, outline_color in reversed(self.colors):
            if self.value/self.to*100 < max_perc:
                return fill_color, outline_color
        return self.fill_color, self.outline_color
    
    def draw(self, surface: pygame.Surface) -> None:
        if self.orient.lower() in ["h", "horizontal"]:
            self.render_horiontal(surface)
        elif self.orient.lower() in ["v", "vertical"]:
            self.render_vertical(surface)
        else:
            raise ValueError(f"Invalid orient {self.orient}. Must be 'h' or 'v'.")
        