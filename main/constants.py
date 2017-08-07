import os

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = "{}/..".format(THIS_FILE_PATH)

MAIN_FONT = '{}/resources/fonts/retrofitted.ttf'.format(PROJECT_ROOT)

IMAGES_FOLDER = '{}/resources/images'.format(PROJECT_ROOT)
SOUND_FOLDER = '{}/resources/sound'.format(PROJECT_ROOT)

DEFAULT_STEP = 4

SCREEN_W = 640
SCREEN_H = 480

FPS = 60

SCORE_FOLDER = "~/.snake_python"
SCORE_FILE = SCORE_FOLDER + "/scores.json"
