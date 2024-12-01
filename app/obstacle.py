import pygame
from random import randint

from app.stages import Stage


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, stage: Stage):
        super().__init__()
        snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
        self.frames = [snail_frame_1, snail_frame_2]
        self.y_movement = 5
        self.angle = 0
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(800, 900), 300))
        self.x_movement = -6
        self.collided_with_player = False
        self.stage: Stage = stage

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def movement(self):
        self.rect.x += self.x_movement

    def update(self):
        self.animation_state()
        self.movement()
        self.bumps_into_obstacle()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100 or self.rect.x > 850:
            self.kill()

    def change_direction(self):
        snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()

        self.frames = [pygame.transform.flip(snail_frame_1, True, False),
                       pygame.transform.flip(snail_frame_2, True, False)]
        self.x_movement = 6

    def set_collided_with_player(self, collided):
        self.collided_with_player = collided

    def first_collision(self):
        return not self.collided_with_player

    def bumps_into_obstacle(self):
        hits = pygame.sprite.spritecollide(self, self.stage.box_group, False)
        if hits:
            if self.collide_on_sides():
                self.change_direction()

    def collide_on_sides(self):
        return self.rect.collidepoint(self.stage.box_group.sprite.rect.midright) or \
               self.rect.collidepoint(self.stage.box_group.sprite.rect.bottomright) or \
               self.rect.collidepoint(self.stage.box_group.sprite.rect.midleft) or \
               self.rect.collidepoint(self.stage.box_group.sprite.rect.bottomleft)
