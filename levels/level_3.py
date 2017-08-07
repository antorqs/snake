from levels.base_level import BaseLevel
from utils import image_util as iu
from main.constants import IMAGES_FOLDER, SOUND_FOLDER
from sprites.snake_sprite import Obstacle


class Level3(BaseLevel):
    def __init__(self):
        super().__init__()
        self.max_score = 16
        self.level_name = 'level1'
        self.stone = "{}/stone.png".format(IMAGES_FOLDER)
        self.stone_image = iu.load_image(self.stone)

        self.portal = "{}/portal.png".format(IMAGES_FOLDER)
        self.portal_image = iu.load_image(self.portal)

        self.wall_image = iu.load_image(self.wall)
        self.ground_image = iu.load_image(self.ground)

        self.rock_positions = [
            (350, 250),
            (150, 150),
            (550, 50),
            (420, 80),
            (370, 120),
            (250, 90),
            (150, 110),
            (250, 200),
            (150, 410),
        ]

        self.portal1 = None
        self.portal2 = None

        self.construct()

        self.next_level = None
        self.song = "{}/level3.ogg".format(SOUND_FOLDER)

    def construct(self):
        super().construct()
        for rp in self.rock_positions:
            self.add_rock(rp[0], rp[1])

        self.portal1 = Obstacle(400, 180, image=self.portal_image)
        self.portal2 = Obstacle(200, 200, image=self.portal_image)
        self.all_sprites.add(self.portal1)
        self.all_sprites.add(self.portal2)
        self.portals.add(self.portal1, self.portal2)

    def add_rock(self, x, y):
        stone = Obstacle(x, y, image=self.stone_image)
        self.all_sprites.add(stone)
        self.obstacles.add(stone)

    def draw(self, screen):
        super().draw(screen)

