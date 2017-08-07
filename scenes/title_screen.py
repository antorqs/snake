import pygame
from pygame_base.game_base import SceneBase
import utils.text_util as tu
import main.constants as constants
from scenes.about_scene import AboutScene
from scenes.game_scene import GameScene
from levels.level_0 import Level0
from levels.level_1 import Level1
from levels.endless import Endless
from main.constants import SOUND_FOLDER


class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

        self.name = "Title"
        self.selected = 1
        self.max_options = 3
        self.scenes = [
            GameScene(Level1()),
            GameScene(Endless()),
            AboutScene(self),
        ]

        self.level_0 = Level0()
        self.song = "{}/title.ogg".format(SOUND_FOLDER)
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.song)
            pygame.mixer.music.play(1)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.switch_to_scene(self.scenes[self.selected - 1])
                elif event.key == pygame.K_DOWN:
                    self.selected = self.selected + 1 if self.selected < self.max_options else 1
                elif event.key == pygame.K_UP:
                    self.selected = self.selected - 1 if self.selected > 1 else self.max_options

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.level_0.bg_surface, (0, 0))
        title = tu.create_text("SNAkE!", constants.MAIN_FONT, 72, (255, 255, 255))
        selected = tu.create_text(".", constants.MAIN_FONT, 60, (255, 255, 255))

        options = [
            tu.create_text("Story Game", constants.MAIN_FONT, 50, (255, 255, 255)),
            tu.create_text("Endless Game", constants.MAIN_FONT, 50, (255, 255, 255)),
            tu.create_text("About", constants.MAIN_FONT, 50, (255, 255, 255))
        ]

        vertical_position = 100

        screen.blit(title,
                    ((constants.SCREEN_W - title.get_width()) // 2,
                     vertical_position))

        vertical_position += 150
        h_half = constants.SCREEN_W // 2
        for option in options:
            screen.blit(option,
                        (h_half - 120,
                         vertical_position))
            vertical_position += 50

        screen.blit(selected,
                    (h_half - 170,
                     230 + (self.selected * 50 - 50)))
