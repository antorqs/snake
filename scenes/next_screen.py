import pygame
import json
import os
from pygame_base.game_base import SceneBase
import utils.text_util as tu
import main.constants as constants
import scenes
from levels.level_0 import Level0


class NextLevelScene(SceneBase):
    def __init__(self, level, score, next_level):
        SceneBase.__init__(self)
        self.level = level
        self.score = score
        self.next_level = next_level
        self.max_score = 0

        self.store_score()

        self.name = "Next"
        self.level_0 = Level0()
        self.song = "{}/title.ogg".format(constants.SOUND_FOLDER)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.switch_to_scene(scenes.game_scene.GameScene(self.next_level))

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.level_0.bg_surface, (0, 0))
        title = tu.create_text("Level Completed!", constants.MAIN_FONT, 72, (255, 255, 255))
        your_score = tu.create_text("Your Score!", constants.MAIN_FONT, 30, (255, 255, 255))
        score = tu.create_text(str(self.score), constants.MAIN_FONT, 50, (255, 255, 255))

        press_to_continue = tu.create_text("Press ENTER to continue...",
                                           constants.MAIN_FONT, 30, (255, 255, 255))

        vertical_position = 50
        screen.blit(title,
                    ((constants.SCREEN_W - title.get_width()) // 2,
                     vertical_position))

        vertical_position += 100

        screen.blit(your_score,
                    ((constants.SCREEN_W - your_score.get_width()) // 2,
                     vertical_position))
        vertical_position += 50
        screen.blit(score,
                    ((constants.SCREEN_W - score.get_width()) // 2,
                     vertical_position))

        vertical_position += 100
        screen.blit(press_to_continue,
                    ((constants.SCREEN_W - press_to_continue.get_width()) // 2,
                     vertical_position))

    def get_max_score(self, level):
        max_score = 0
        data = {}
        if os.path.exists(constants.SCORE_FILE):
            with open(constants.SCORE_FILE) as data_file:
                data = json.load(data_file)
                if level in data:
                    max_score = data[level]['max_score']
        self.max_score = max_score
        return data

    def store_score(self):
        max_score_data = self.get_max_score(self.level)
        if self.score > self.max_score:
            max_score_data[self.level] = {}
            max_score_data[self.level]['max_score'] = self.score

            with open(constants.SCORE_FILE, 'w') as fp:
                json.dump(max_score_data, fp)
