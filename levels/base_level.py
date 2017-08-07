import pygame
from main.constants import IMAGES_FOLDER, SCREEN_W, SCREEN_H
from sprites.snake_sprite import Obstacle
import utils.image_util as iu


class BaseLevel:
    def __init__(self):
        self.max_score = None
        self.level_name = 'NONE'
        self.wall = "{}/brick.png".format(IMAGES_FOLDER)
        self.ground = "{}/grass.png".format(IMAGES_FOLDER)

        self.wall_image = iu.load_image(self.wall)
        self.ground_image = iu.load_image(self.ground)

        self.all_sprites = pygame.sprite.OrderedUpdates()
        self.obstacles = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()

        self.bg_surface = pygame.Surface((SCREEN_W, SCREEN_H))
        self.bg_surface = self.bg_surface.convert()

        self.next_level = None

    def construct(self):
        self.construct_ground()
        self.construct_border()

    def construct_ground(self):
        x = 0
        y = 0
        ground_image_w = self.ground_image.get_size()[0]
        ground_image_h = self.ground_image.get_size()[1]
        for ii in range(0, (SCREEN_W // ground_image_w) + 1):
            for jj in range(0, (SCREEN_H // ground_image_h) + 1):
                ground = Obstacle(x, y, image=self.ground_image)
                y += ground_image_h
                self.bg_surface.blit(ground.image, (x, y))

            y = 0
            x += ground_image_w

    def construct_border(self):
        x = 0
        y = 0
        wall_image_w = self.wall_image.get_size()[0]
        wall_image_h = self.wall_image.get_size()[1]
        for ii in range(0, (SCREEN_W // wall_image_w) + 1):
            wall = Obstacle(x, 0, image=self.wall_image)
            # self.all_sprites.add(wall)
            self.obstacles.add(wall)
            self.bg_surface.blit(wall.image, (x, 0))

            wall = Obstacle(x, SCREEN_H - wall_image_h, image=self.wall_image)
            self.obstacles.add(wall)
            self.bg_surface.blit(wall.image, (x, SCREEN_H - wall_image_h))

            x += wall_image_w

        for jj in range(0, (SCREEN_H // wall_image_h) + 1):
            wall = Obstacle(0, y, image=self.wall_image)
            # self.all_sprites.add(wall)
            self.obstacles.add(wall)
            self.bg_surface.blit(wall.image, (0, y))

            wall = Obstacle(SCREEN_W - wall_image_w, y, image=self.wall_image)
            self.obstacles.add(wall)
            self.bg_surface.blit(wall.image, (SCREEN_W - wall_image_w, y))

            y += wall_image_h

    def draw(self, screen):
        self.all_sprites.draw(screen)
