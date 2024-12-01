import pygame
from pygame.sprite import Sprite

from app.player import Player


class LittlePlayer(Player):
    def __init__(self, stage):
        super().__init__(stage)
        self.player_standing_1 = pygame.image.load('graphics/littleag/pose-1.png').convert_alpha()
        self.player_standing_2 = pygame.image.load('graphics/littleag/pose-2.png').convert_alpha()
        self.player_standing_3 = pygame.image.load('graphics/littleag/pose-3.png').convert_alpha()
        self.player_standing_4 = pygame.image.load('graphics/littleag/pose-4.png').convert_alpha()
        self.player_standing = [self.player_standing_1, self.player_standing_2, self.player_standing_3,
                                self.player_standing_4]

        self.player_walk_1 = pygame.image.load('graphics/littleag/littleag-walk1.png').convert_alpha()
        self.player_walk_2 = pygame.image.load('graphics/littleag/littleag-walk1.png').convert_alpha()
        self.player_walk = [self.player_walk_1, self.player_walk_2]

        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/littleag/littleag-jump.png').convert_alpha()
        self.image = self.player_standing[self.player_index]
        self.player_x_position = 10
        self.ground_position = 300
        self.player_y_position = 0
        self.rect = self.image.get_rect(midbottom=(self.player_x_position, self.ground_position))
        self.gravity = 0
        self.player_walking = False
        self.jump_value = 15
        self.lives = 20
        self._top_lives = 20
        # self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')

    def move_to(self, x, offset):
        player_length = int(self.rect.width / 4) + offset
        self.player_x_position = (x - player_length)
        self.rect.x = x

    def reset_lives(self):
        self.lives = 20
