import pygame.sprite
from random import randint


class Medal(pygame.sprite.Sprite):
    def __init__(self, spun_time):
        super().__init__()
        coin_frame_1 = pygame.image.load('graphics/artifacts/coin-1.png').convert_alpha()
        coin_frame_2 = pygame.image.load('graphics/artifacts/coin-2.png').convert_alpha()
        coin_frame_3 = pygame.image.load('graphics/artifacts/coin-3.png').convert_alpha()
        coin_frame_4 = pygame.image.load('graphics/artifacts/coin-4.png').convert_alpha()
        coin_frame_5 = pygame.transform.flip(coin_frame_3, True, False)
        coin_frame_6 = pygame.transform.flip(coin_frame_2, True, False)
        coin_frame_7 = pygame.transform.flip(coin_frame_1, True, False)
        self.frames = [coin_frame_1, coin_frame_2, coin_frame_3, coin_frame_4, coin_frame_5, coin_frame_6, coin_frame_7]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(10, 790), randint(50, 290)))
        self.spun_time = spun_time

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.destroy()

    def destroy(self):
        current_time = int((pygame.time.get_ticks() - self.spun_time) / 1000)
        if current_time > 3:
            self.kill()
