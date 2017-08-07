from levels.base_level import BaseLevel
from utils import image_util as iu
from main.constants import IMAGES_FOLDER, SOUND_FOLDER
from sprites.snake_sprite import Obstacle
from levels.level_3 import Level3


class Level2(BaseLevel):
    def __init__(self):
        super().__init__()
        self.max_score = 12
        self.level_name = 'level1'
        self.stone = "{}/stone.png".format(IMAGES_FOLDER)
        self.stone_image = iu.load_image(self.stone)

        self.portal = "{}/portal.png".format(IMAGES_FOLDER)
        self.portal_image = iu.load_image(self.portal)

        self.wall_image = iu.load_image(self.wall)
        self.ground_image = iu.load_image(self.ground)

        self.rock_positions = [
            (150, 150),
            (350, 350),
            (150, 250),
            (550, 50),
            (250, 90),
            (150, 110),
        ]

        self.portal1 = None
        self.portal2 = None

        self.construct()

        self.next_level = Level3()
        self.song = "{}/level2.ogg".format(SOUND_FOLDER)

    def construct(self):
        super().construct()
        for rp in self.rock_positions:
            self.add_rock(rp[0], rp[1])

        self.portal1 = Obstacle(200, 250, image=self.portal_image)
        self.portal2 = Obstacle(80, 400, image=self.portal_image)
        self.all_sprites.add(self.portal1)
        self.all_sprites.add(self.portal2)
        self.portals.add(self.portal1, self.portal2)

    def add_rock(self, x, y):
        stone = Obstacle(x, y, image=self.stone_image)
        self.all_sprites.add(stone)
        self.obstacles.add(stone)

    def draw(self, screen):
        super().draw(screen)

