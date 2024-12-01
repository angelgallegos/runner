from app.obstacle import Obstacle
import pygame
import math
from random import randint, choice

from app.stages import Stage


class Fly(Obstacle):
    def __init__(self, stage: Stage):
        super().__init__(stage)
        fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
        fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
        self.frames = [fly_frame_1, fly_frame_2]
        self.y_movement = 5
        self.angle = 0
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(800, 900), 110))
        self.bottom_limit = choice([125, 150, 175, 200, 225, 250])
        self.x_movement = -6

    def movement(self):
        self.rect.x += self.x_movement
        # if self.rect.x >= 400:
        #     if self.obstacle_type == 'fly':
        #         self.move_in_circle(400)
        #     else:
        #         self.move_normal()
        # else:

        if self.rect.y == 75:
            self.y_movement = 5
        if self.rect.y == self.bottom_limit:
            self.y_movement = -5

        self.rect.y += self.y_movement

    def move_in_circle(self, start_on_x):
        self.rect.x = int(math.cos(self.angle) * 100) + start_on_x
        self.rect.y = int(math.sin(self.angle) * 100) + 100
        self.angle += 0.05

    def change_direction(self):
        fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
        fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()

        self.frames = [pygame.transform.flip(fly_frame_1, True, False),
                       pygame.transform.flip(fly_frame_2, True, False)]
        self.x_movement = 6
