import pygame
from pygame.sprite import Sprite
from main.constants import IMAGES_FOLDER
from utils import image_util as iu
import main.constants as constants


class SnakeBody(Sprite):
    def __init__(self, x, y, head=False, name=None):
        super().__init__()
        self.ported = 0
        self.name = name
        self.direction = 'R'
        self.next_direction = 'R'
        self.is_head = head
        self.following = None
        if self.is_head:
            self.image = iu.load_image("{}/snake_head.png".format(IMAGES_FOLDER))
        else:
            self.image = iu.load_image("{}/snake_body.png".format(IMAGES_FOLDER))

        self.original_image = self.image
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.moved = 0

    def set_direction(self, direction):
        self.direction = direction
        self.rotate_body_part(direction)

    def set_next_direction(self, direction):
        self.next_direction = direction

    def rotate_body_part(self, direction):
        if direction == "R":
            self.image = self.original_image
        if direction == "L":
            self.image = pygame.transform.rotate(self.original_image, 180)
        if direction == "U":
            self.image = pygame.transform.rotate(self.original_image, 90)
        if direction == "D":
            self.image = pygame.transform.rotate(self.original_image, 270)
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.direction == 'R':
            self.rect.x += constants.DEFAULT_STEP
        if self.direction == 'L':
            self.rect.x -= constants.DEFAULT_STEP
        if self.direction == 'U':
            self.rect.y -= constants.DEFAULT_STEP
        if self.direction == 'D':
            self.rect.y += constants.DEFAULT_STEP

        self.moved += constants.DEFAULT_STEP
        if self.following is not None:
            self.following.set_next_direction(self.direction)

        if self.moved >= self.rect.width:
            combination = "{}{}".format(self.direction, self.next_direction)
            if combination not in ['UD', 'DU', 'RL', 'LR']:
                    self.set_direction(self.next_direction)
            self.moved = 0

    def set_following(self, following):
        self.following = following


class Fruit(Sprite):
    def __init__(self, fruit="apple"):
        super().__init__()
        self.image = iu.load_image("{}/{}.png".format(IMAGES_FOLDER, fruit))
        self.rect = self.image.get_rect()
        self.iterations = 0


class Obstacle(Sprite):
    def __init__(self, x, y, image=None, image_path=None):
        super().__init__()
        self.image = iu.load_image("{}/{}".format(IMAGES_FOLDER, image_path)) if image is None else image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
