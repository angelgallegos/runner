from typing import Optional

import pygame
from pygame import Surface, Rect

from app.enums import PlatformType


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image: Surface
        self.rect: Rect
        self.type: Optional[PlatformType] = None
        self.x_movement = 0

