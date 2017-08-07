import os
from scenes.title_screen import TitleScene
from pygame_base.game_base import initialize, run_game
import main.constants as constants

if not os.path.exists(constants.SCORE_FOLDER):
    os.makedirs(constants.SCORE_FOLDER)

screen = initialize(constants.SCREEN_W, constants.SCREEN_H)
run_game(screen, constants.FPS, TitleScene())
