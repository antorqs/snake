from levels.base_level import BaseLevel
from utils import image_util as iu
from main.constants import IMAGES_FOLDER
from sprites.snake_sprite import Obstacle


class Level0(BaseLevel):
    def __init__(self):
        super().__init__()

        self.wall_image = iu.load_image(self.wall)
        self.ground_image = iu.load_image(self.ground)

        self.construct()

    def construct(self):
        super().construct()

    def draw(self, screen):
        super().draw(screen)

