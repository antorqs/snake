import pygame
import random
import os
import json
from pygame_base.game_base import SceneBase
from scenes.game_over_screen import GameOverScene
from scenes.next_screen import NextLevelScene
from sprites.snake_sprite import SnakeBody, Fruit
from utils import text_util as tu
from utils import sound_util as su
import main.constants as constants


class GameScene(SceneBase):
    def __init__(self, level):
        SceneBase.__init__(self)

        self.name = "Game"
        self.score = 0
        self.fruits_eaten = 0
        self.player = Player()
        self.all_sprites_list = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.super_fruits = pygame.sprite.Group()

        self.apple = Fruit("apple")
        self.super_apple = Fruit("super_apple")
        self.super_fruits_count = 0

        self.current_level = level
        self.level_max_score = 0
        self.get_max_score(level.level_name)

        self.song = self.current_level.song

        self.eat_effect = "{}/eat.ogg".format(constants.SOUND_FOLDER)
        self.teleport_effect = "{}/teleport.ogg".format(constants.SOUND_FOLDER)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and self.player.direction != 'U':
                    self.player.set_direction('D')
                if event.key == pygame.K_UP and self.player.direction != 'D':
                    self.player.set_direction('U')
                if event.key == pygame.K_LEFT and self.player.direction != 'R':
                    self.player.set_direction('L')
                if event.key == pygame.K_RIGHT and self.player.direction != 'L':
                    self.player.set_direction('R')
                pass

    def update(self):
        if self.player.alive:
            self.player.move()

            if len(self.fruits) == 0 and len(self.super_fruits) == 0:
                correct = False
                while not correct:
                    self.apple.rect.x = random.randint(40, 570)
                    self.apple.rect.y = random.randint(40, 410)
                    obstacle_overlap = pygame.sprite.spritecollide(self.apple, self.current_level.obstacles, False)
                    snake_overlap = pygame.sprite.spritecollide(self.apple, self.player.complete_snake, False)
                    portal_overlap = pygame.sprite.spritecollide(self.apple, self.current_level.portals, False)
                    correct = len(obstacle_overlap) == 0 and len(snake_overlap) == 0 and len(portal_overlap) == 0

                self.apple.dirty = 1
                self.fruits.add(self.apple)

                if self.super_fruits_count < 3:
                    super_fruit_probability = random.randint(0, 10)
                    if super_fruit_probability > 6:
                        correct = False
                        while not correct:
                            self.super_apple.rect.x = random.randint(40, 570)
                            self.super_apple.rect.y = random.randint(40, 410)
                            obstacle_overlap = \
                                pygame.sprite.spritecollide(self.super_apple,
                                                            self.current_level.obstacles, False)
                            snake_overlap = \
                                pygame.sprite.spritecollide(self.super_apple,
                                                            self.player.complete_snake, False)

                            portal_overlap = \
                                pygame.sprite.spritecollide(self.super_apple,
                                                            self.current_level.portals, False)

                            correct = len(obstacle_overlap) == 0 and len(snake_overlap) == 0 and len(portal_overlap) == 0
                        self.super_apple.dirty = 1
                        self.super_fruits_count += 1
                        self.super_fruits.add(self.super_apple)

            elif len(self.super_fruits) > 0:
                self.super_apple.iterations += 1
                if self.super_apple.iterations >= 180:
                    self.super_apple.iterations = 0
                    self.super_fruits.remove(self.super_apple)

            # CHECK IF SNAKE ATE
            fruits_hit = pygame.sprite.spritecollide(self.player.head, self.fruits, True)
            super_fruits_hit = pygame.sprite.spritecollide(self.player.head, self.super_fruits, True)

            if len(fruits_hit):
                su.play_sound(self.eat_effect)
                self.player.grow()
                self.score += 1
                self.fruits_eaten += 1
            if len(super_fruits_hit):
                su.play_sound(self.eat_effect)
                self.player.grow()
                self.score += 3
                self.super_apple.iterations = 0

            # CHECK IF SNAKE HIT OBSTACLE
            obstacles_hit = pygame.sprite.spritecollide(self.player.head, self.current_level.obstacles, False)
            body_hit = pygame.sprite.spritecollide(self.player.head, self.player.snake_body, False)

            if len(obstacles_hit) or len(body_hit):
                self.player.alive = 0
                self.switch_to_scene(GameOverScene(self.current_level.level_name, self.score))

            # CHECK IF SNAKE ENTERED PORTAL
            for body_part in self.player.complete_snake:
                portals_hit = pygame.sprite.spritecollide(body_part, self.current_level.portals, False)

                if len(portals_hit) > 0:
                    if body_part.ported == 0:
                        next_portal = [_ for _ in self.current_level.portals if _ not in portals_hit][0]
                        self.current_level.portals.add(portals_hit)
                        body_part.rect.x = next_portal.rect.x
                        body_part.rect.y = next_portal.rect.y
                        body_part.ported = 1

                        if body_part == self.player.head:
                            su.play_sound(self.teleport_effect)
                else:
                    body_part.ported = 0

            # CHECK IF SNAKE WON
            if self.current_level.max_score is not None and self.fruits_eaten >= self.current_level.max_score:
                if self.current_level.next_level is not None:
                    self.switch_to_scene(NextLevelScene(self.current_level.level_name, self.score,
                                                        self.current_level.next_level))
                else:
                    self.switch_to_scene(GameOverScene(self.current_level.level_name, self.score, lose=False))

    def render(self, screen):
        # screen.fill((255, 255, 255))
        score_word = tu.create_text("Score: ", constants.MAIN_FONT, 25, (255, 255, 255))
        points = tu.create_text(str(self.score), constants.MAIN_FONT, 25, (255, 255, 255))
        max_score_word = tu.create_text("Max Score: ", constants.MAIN_FONT, 25, (255, 255, 255))
        max_points = tu.create_text(str(self.level_max_score), constants.MAIN_FONT, 25, (255, 255, 255))
        screen.blit(self.current_level.bg_surface, (0, 0))
        screen.blit(score_word, (5, 5))
        screen.blit(points, (100, 5))
        screen.blit(max_score_word, (420, 5))
        screen.blit(max_points, (600, 5))
        self.current_level.draw(screen)
        self.player.draw_snake(screen)
        self.fruits.draw(screen)
        self.super_fruits.draw(screen)

    def get_max_score(self, level):
        max_score = 0
        data = {}
        if os.path.exists(constants.SCORE_FILE):
            with open(constants.SCORE_FILE) as data_file:
                data = json.load(data_file)
                if level in data:
                    max_score = data[level]['max_score']
        self.level_max_score = max_score
        return data


class Player:
    def __init__(self):
        self.alive = True
        self.head = SnakeBody(x=100, y=50, head=True, name="1")
        self.complete_snake = pygame.sprite.OrderedUpdates()
        self.snake_body = pygame.sprite.OrderedUpdates()
        self.complete_snake.add(self.head)

        self.last = self.head
        self.direction = 'R'
        self.grow(False)
        self.grow()
        self.grow()

    def set_direction(self, direction):
        head = self.head
        self.direction = direction
        head.set_next_direction(direction)

    def move(self):
        self.complete_snake.update()

    def draw_snake(self, screen):
        self.complete_snake.draw(screen)

    def grow(self, hittable=True):
        last = self.last
        width = last.rect.width
        x = last.rect.x
        y = last.rect.y
        if last.direction == "R":
            x -= width
        elif last.direction == "L":
            x += width
        elif last.direction == "D":
            y -= width
        elif last.direction == "U":
            y += width
        name = len(self.snake_body) + 1
        new_tail = SnakeBody(x=x, y=y, name=name)
        new_tail.set_direction(last.direction)
        new_tail.set_next_direction(last.direction)
        new_tail.moved = last.moved
        last.set_following(new_tail)
        if hittable:
            self.snake_body.add(new_tail)
        self.complete_snake.add(new_tail)
        self.last = new_tail
