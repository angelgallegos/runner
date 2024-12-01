import pygame

from app.enums import PlatformType
from app.platform import Platform


class Box(Platform):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/artifacts/box-1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(380, 300))
        self.type = PlatformType.STATIC
