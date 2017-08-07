import pygame
import json
import os
from pygame_base.game_base import SceneBase
import utils.text_util as tu
import main.constants as constants
import scenes
from levels.level_0 import Level0


class GameOverScene(SceneBase):
    def __init__(self, level, score=0, lose=True):
        SceneBase.__init__(self)

        self.level = level
        self.score = score
        self.max_score = 0

        self.lose = lose

        self.store_score()

        self.name = "Game Over"
        self.selected = 1
        self.max_options = 2
        self.scenes = [
            scenes.title_screen.TitleScene(),
            None
        ]
        self.level_0 = Level0()

        self.song = "{}/game_over.ogg".format(constants.SOUND_FOLDER)

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
        text = "GAME OVER!"
        if not self.lose:
            text = "GAME COMPLETED!"
        title = tu.create_text(text, constants.MAIN_FONT, 72, (255, 255, 255))
        your_score = tu.create_text("Your Score!", constants.MAIN_FONT, 30, (255, 255, 255))
        score = tu.create_text(str(self.score), constants.MAIN_FONT, 50, (255, 255, 255))

        selected = tu.create_text(".", constants.MAIN_FONT, 60, (255, 255, 255))

        options = [
            tu.create_text("Restart Game", constants.MAIN_FONT, 50, (255, 255, 255)),
            tu.create_text("Exit", constants.MAIN_FONT, 50, (255, 255, 255))
        ]

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
        selection_position = vertical_position - 20
        h_half = constants.SCREEN_W // 2
        for option in options:
            screen.blit(option,
                        (h_half - 120,
                         vertical_position))
            vertical_position += 50

        screen.blit(selected,
                    (h_half - 170,
                     selection_position + (self.selected * 50 - 50)))

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
