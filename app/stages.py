import pygame
from pygame.sprite import GroupSingle, Group, Sprite

from app.box import Box
from app.moving_platform import MovingBox
from app.platform import Platform


class Stage:
    def __init__(self):
        self.box_group: Group = GroupSingle()
        self.box = Box()
        self.box_group.add(self.box)

        self.moving_box_group = pygame.sprite.GroupSingle()
        self.moving_box = MovingBox()
        self.moving_box_group.add(self.moving_box)

        self.obstacle_group = pygame.sprite.Group()

        self.medal_group = pygame.sprite.Group()

        #self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
        self.sky_surface = pygame.image.load('graphics/backgrounds/background-1.png').convert()
        self.ground_surface = pygame.image.load('graphics/ground.png').convert()

        self.sky_coordinates = (0, 0)
        self.ground_coordinates = (0, 300)
        self.available_time = 120
        self.required_coins = 10

    def add_box(self, box: Platform):
        self.box_group.add(box)
