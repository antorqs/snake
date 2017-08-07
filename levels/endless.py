from levels.base_level import BaseLevel
from utils import image_util as iu
from main.constants import IMAGES_FOLDER, SOUND_FOLDER
from sprites.snake_sprite import Obstacle


class Endless(BaseLevel):
    def __init__(self):
        super().__init__()

        self.stone = "{}/stone.png".format(IMAGES_FOLDER)
        self.stone_image = iu.load_image(self.stone)

        self.portal = "{}/portal.png".format(IMAGES_FOLDER)
        self.portal_image = iu.load_image(self.portal)

        self.wall_image = iu.load_image(self.wall)
        self.ground_image = iu.load_image(self.ground)

        self.construct()
        self.level_name = 'endless'
        self.song = "{}/level3.ogg".format(SOUND_FOLDER)

        self.portal1 = None
        self.portal2 = None

    def construct(self):
        super().construct()
        self.add_rock(80, 220)
        self.add_rock(560, 220)
        self.add_rock(800, 380)
        self.add_rock(420, 420)
        self.add_rock(490, 80)
        self.add_rock(300, 240)
        self.add_rock(410, 180)

        self.portal1 = Obstacle(100, 100, image=self.portal_image)
        self.portal2 = Obstacle(540, 380, image=self.portal_image)
        self.all_sprites.add(self.portal1)
        self.all_sprites.add(self.portal2)
        self.portals.add(self.portal1, self.portal2)

    def add_rock(self, x, y):
        stone = Obstacle(x, y, image=self.stone_image)
        self.all_sprites.add(stone)
        self.obstacles.add(stone)

    def draw(self, screen):
        super().draw(screen)

