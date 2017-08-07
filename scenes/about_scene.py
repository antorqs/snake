import main.constants as constants
from pygame_base.game_base import SceneBase
import utils.text_util as tu
import pygame
from levels.level_0 import Level0


class AboutScene(SceneBase):
    def __init__(self, title_scene):
        SceneBase.__init__(self)
        self.name = "About"
        self.title_scene = title_scene
        self.level_0 = Level0()
        self.song = "{}/about.ogg".format(constants.SOUND_FOLDER)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.switch_to_scene(self.title_scene)

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.level_0.bg_surface, (0, 0))
        title = tu.create_text("Snake!", constants.MAIN_FONT, 72, (255, 255, 255))
        powered_by = tu.create_text("Developed with Pygame", constants.MAIN_FONT, 30, (255, 255, 255))
        author = tu.create_text("@antorqs", constants.MAIN_FONT, 50, (255, 255, 255))
        credits_ = tu.create_text("Please check README file for credits", constants.MAIN_FONT, 20, (255, 255, 255))

        press_to_continue = tu.create_text("Press ENTER to continue...",
                                           constants.MAIN_FONT, 30, (255, 255, 255))

        vertical_position = 50
        screen.blit(title,
                    ((constants.SCREEN_W - title.get_width()) // 2,
                     vertical_position))

        vertical_position += 100
        screen.blit(powered_by,
                    ((constants.SCREEN_W - powered_by.get_width()) // 2,
                     vertical_position))
        vertical_position += 50
        screen.blit(author,
                    ((constants.SCREEN_W - author.get_width()) // 2,
                     vertical_position))

        vertical_position += 50
        screen.blit(credits_,
                    ((constants.SCREEN_W - credits_.get_width()) // 2,
                     vertical_position))
        vertical_position += 100
        screen.blit(press_to_continue,
                    ((constants.SCREEN_W - press_to_continue.get_width()) // 2,
                     vertical_position))
