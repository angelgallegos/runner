import pygame
from sys import exit
from random import choice
from app.factory.obstacle_factory import ObstacleFactory
from app.littleplayer import LittlePlayer
from app.medal import Medal
from app.player import Player
from app.stages import Stage


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.start_time = 0
        self.started = False
        self.game_active = False
        self.game_paused = False
        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption('Alien Runner')
        self.stage = Stage()
        self.player = Player(self.stage)

        self.player_group = pygame.sprite.GroupSingle()
        # self.player = LittlePlayer(self.stage)
        self.player_group.add(self.player)

        # Timers
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

        self.medal_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.medal_timer, 2000)

        self.test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active is False:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                        self.game_active = True
                        self.started = True
                        self.player.reset_lives()
                        self.start_time = pygame.time.get_ticks()
                        self.player.coins = 0

                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.game_paused = not self.game_paused

                if self.game_active:
                    if event.type == self.obstacle_timer:
                        self.stage.obstacle_group.add(
                            ObstacleFactory().create(choice(['fly', 'fly', 'fly', 'snail', 'snail', 'snail', 'snail']),
                                                     self.stage))

                    if event.type == self.medal_timer:
                        self.stage.medal_group.add(Medal(pygame.time.get_ticks()))

            if self.game_active and not self.game_paused:
                self.screen.blit(self.stage.sky_surface, self.stage.sky_coordinates)
                self.screen.blit(self.stage.ground_surface, self.stage.ground_coordinates)

                time = self.display_timer()
                self.display_coins()

                self.stage.box_group.draw(self.screen)
                self.stage.box_group.update()

                self.player_group.draw(self.screen)
                self.player_group.update()
                self.stage.obstacle_group.draw(self.screen)
                self.stage.obstacle_group.update()
                self.stage.medal_group.draw(self.screen)
                self.stage.medal_group.update()

                self.stage.moving_box_group.draw(self.screen)
                self.stage.moving_box_group.update()
                self.player.collision_sprite()
                self.display_health(self.player)
                if self.player.lives == 0 or time < 1:
                    self.game_active = False
                    self.stage.obstacle_group.empty()
                    # obstacle_timer = speed_up_timer(obstacle_timer)
                self.player.update_speed(5)
            else:
                if self.game_paused:
                    self.inactive_screen()
                else:
                    if not self.started:
                        self.inactive_screen()
                    else:
                        if self.player.coins < self.stage.required_coins:
                            self.failed_stage()
                        else:
                            self.succedeed_stage()

            pygame.display.update()
            self.clock.tick(60)

    def inactive_screen(self):
        game_name = self.test_font.render('Alien Runner', False, (111, 196, 169))
        game_name_rectangle = game_name.get_rect(center=(400, 80))
        self.screen.fill((94, 129, 162))
        player_stand = pygame.image.load('graphics/Player/alien_stand.png')
        player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        player_stand_rectangle = player_stand.get_rect(center=(400, 200))
        self.screen.blit(player_stand, player_stand_rectangle)
        self.player.back_to_zero()
        self.screen.blit(game_name, game_name_rectangle)
        game_message = self.test_font.render('Press \'S\' to start', False, (111, 196, 169))
        game_message_rectangle = game_message.get_rect(center=(400, 340))
        self.screen.blit(game_message, game_message_rectangle)

    def failed_stage(self):
        self.player.back_to_zero()
        game_name = self.test_font.render('Alien Runner', False, (111, 196, 169))
        game_name_rectangle = game_name.get_rect(center=(400, 80))
        self.screen.fill((94, 129, 162))
        player_stand = pygame.image.load('graphics/Player/alien_stand.png')
        player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        player_stand_rectangle = player_stand.get_rect(center=(400, 200))
        self.screen.blit(player_stand, player_stand_rectangle)
        score_message = self.test_font.render(f'You failed to collect the required coins', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        game_message = self.test_font.render('Press \'S\' to play again', False, (111, 196, 169))
        game_message_rect = score_message.get_rect(center=(500, 370))
        self.screen.blit(game_name, game_name_rectangle)
        self.screen.blit(score_message, score_message_rect)
        self.screen.blit(game_message, game_message_rect)

    def succedeed_stage(self):
        self.player.back_to_zero()
        game_name = self.test_font.render('Alien Runner', False, (111, 196, 169))
        game_name_rectangle = game_name.get_rect(center=(400, 80))
        self.screen.fill((94, 129, 162))
        player_stand = pygame.image.load('graphics/Player/alien_stand.png')
        player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        player_stand_rectangle = player_stand.get_rect(center=(400, 200))
        self.screen.blit(player_stand, player_stand_rectangle)
        score_message = self.test_font.render(f'YOU WIN!!!', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        game_message = self.test_font.render('Press \'S\' to play again', False, (111, 196, 169))
        game_message_rect = score_message.get_rect(center=(340, 370))
        self.screen.blit(game_name, game_name_rectangle)
        self.screen.blit(score_message, score_message_rect)
        self.screen.blit(game_message, game_message_rect)

    def display_timer(self):
        current_time = self.stage.available_time - int((pygame.time.get_ticks() - self.start_time) / 1000)
        time_surface = self.test_font.render(f'Time: {current_time}', False, (64, 64, 64))
        time_rectangle = time_surface.get_rect(center=(100, 30))
        self.screen.blit(time_surface, time_rectangle)
        return current_time

    def display_coins(self):
        time_surface = self.test_font.render(f'Coins: {self.player.coins}', False, (64, 64, 64))
        time_rectangle = time_surface.get_rect(center=(375, 30))
        self.screen.blit(time_surface, time_rectangle)

    def display_health(self, player):
        full_heart_surface = pygame.image.load('graphics/artifacts/full-hart.png').convert_alpha()
        half_heart_surface = pygame.image.load('graphics/artifacts/half-hart.png').convert_alpha()
        x = 775 - (25*int(player.top_lives/2))
        for h in range(0, int(player.lives/2)):
            full_heart_rectangle = full_heart_surface.get_rect(center=(x, 30))
            self.screen.blit(full_heart_surface, full_heart_rectangle)
            x += 25
        if player.lives % 2 > 0:
            half_heart_rectangle = half_heart_surface.get_rect(center=(x, 30))
            self.screen.blit(half_heart_surface, half_heart_rectangle)
