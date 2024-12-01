import pygame
from typing import Optional
from pygame.sprite import Sprite

from app.enums import PlatformType
from app.platform import Platform
from app.stages import Stage


class Player(Sprite):
    def __init__(self, stage: Stage):
        super().__init__()
        self.stage: Stage = stage
        self.speed = 5
        self.player_walk_1 = pygame.image.load('graphics/Player/alien_walk_1.png').convert_alpha()
        self.player_walk_2 = pygame.image.load('graphics/Player/alien_walk_2.png').convert_alpha()
        self.player_walk = [self.player_walk_1, self.player_walk_2]
        self.player_standing = [pygame.image.load('graphics/Player/alien_stand.png').convert_alpha()]

        self.player_walk = [self.player_walk_1, self.player_walk_2]

        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/alien_jump.png').convert_alpha()
        self.image = self.player_standing[self.player_index]
        self.player_x_position = 10
        self.ground_position = self.stage.ground_coordinates[1]
        self.rect = self.image.get_rect(midbottom=(self.player_x_position, self.ground_position))
        self.gravity = 0
        self.player_walking = False

        self.jump_value = 20
        # self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.platform_on: Optional[Platform] = None
        self.lives = 10
        self._top_lives = 10
        self.coins = 0

    @property
    def top_lives(self):
        return self._top_lives

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= self.ground_position:
            self.gravity -= self.jump_value
            self.fall_from_platform()
            # self.jump_sound.play()
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            self.player_walking = True
            if keys[pygame.K_RIGHT]:
                self.player_x_position += self.speed
            if keys[pygame.K_LEFT]:
                self.player_x_position -= self.speed
        else:
            self.player_walking = False

    def apply_gravity(self):
        self.rect.y += self.gravity
        if self.rect.bottom >= self.ground_position:
            self.rect.bottom = self.ground_position
            self.gravity = 0
        self.gravity += 1

    def move_x_axis(self):
        self.rect.x = self.player_x_position
        if self.rect.left <= 0:
            self.player_x_position = 1
        if self.rect.right >= 800 and not self.on_moving_platform():
            self.back_to_zero()

    def back_to_zero(self):
        self.player_x_position = 0
        self.rect.bottomleft = (self.player_x_position, self.ground_position)

    def fall_from_platform(self):
        if self.platform_on is not None:
            if self.rect.left > self.platform_on.rect.right or self.rect.right < self.platform_on.rect.left:
                self.ground_position = self.stage.ground_coordinates[1]
                self.player_x_position = self.rect.x
                self.platform_on = None

    def update(self):
        self.player_input()
        self.move_x_axis()
        self.apply_gravity()
        self.interact_with_platform()
        self.fall_from_platform()
        self.move_alone()
        self.collect_coin()
        self.animation_state()

    def on_moving_platform(self):
        return self.platform_on is not None and self.platform_on.type is PlatformType.MOVING

    def move_alone(self):
        if self.on_moving_platform() and self.gravity == 1:
            self.player_x_position += self.platform_on.x_movement

    def move_to(self, x, offset):
        player_length = int(self.rect.width/16) + offset
        self.player_x_position = (x-player_length)
        self.rect.x = x

    def move_to_platform(self, platform: Platform):
        self.platform_on = platform
        self.rect.midbottom = self.platform_on.rect.midtop
        self.ground_position = self.platform_on.rect.y
        self.apply_gravity()

    def update_speed(self, x_movement):
        self.speed = x_movement

    def animation_state(self):
        if self.rect.bottom < self.ground_position:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_walking:
                if self.player_index >= len(self.player_walk):
                    self.player_index = 0
                self.image = self.player_walk[int(self.player_index)]
            else:
                if self.player_index >= len(self.player_standing):
                    self.player_index = 0
                self.image = self.player_standing[int(self.player_index)]

    def collision_sprite(self):
        hits = pygame.sprite.spritecollide(self, self.stage.obstacle_group, False)
        collided = False
        if hits:
            for obstacle in hits:
                if obstacle.first_collision():
                    obstacle.set_collided_with_player(True)
                    obstacle.change_direction()
                    collided = True
                else:
                    collided = False
        else:
            collided = False

        if collided:
            pygame.time.wait(250)
            self.lives -= 1

    def reset_lives(self):
        self.lives = 10

    def interact_with_platform(self):
        if pygame.sprite.spritecollide(self, self.stage.box_group, False):
            if self.rect.collidepoint(self.stage.box.rect.midtop):
                self.move_to_platform(self.stage.box)
            else:
                self.update_speed(0)
                x = self.rect.x
                if x >= (self.stage.box.rect.right - (self.stage.box.rect.w - 1)):
                    self.move_to(self.stage.box.rect.right, -1)
                if x < self.stage.box.rect.left:
                    self.move_to(x, 1)

        if pygame.sprite.spritecollide(self, self.stage.moving_box_group, False):
            if self.rect.collidepoint(self.stage.moving_box.rect.midtop):
                self.move_to_platform(self.stage.moving_box)
            else:
                self.update_speed(0)
                x = self.rect.x
                if x >= (self.stage.moving_box.rect.right - (self.stage.moving_box.rect.w - 1)):
                    self.move_to(self.stage.moving_box.rect.right, -1)
                if x < self.stage.moving_box.rect.left:
                    self.move_to(x, 1)

    def coins_collected(self):
        return self.coins

    def collect_coin(self):
        hits = pygame.sprite.spritecollide(self, self.stage.medal_group, False)
        if hits:
            self.coins += 1
            hits[0].kill()
