import pygame

from app.enums import PlatformType
from app.platform import Platform


class MovingBox(Platform):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/artifacts/moving-box.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(810, 130))
        self.x_movement = -2
        self.stage_y_edges = (0, 800)
        self.type = PlatformType.MOVING

    def movement(self):
        if self.rect.left <= self.stage_y_edges[0]:
            self.change_direction(2)
        if self.rect.right >= self.stage_y_edges[1]:
            self.change_direction(-2)
        self.rect.x += self.x_movement

    def update(self):
        self.movement()

    def change_direction(self, movement):
        self.x_movement = movement
