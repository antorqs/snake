import pygame


class SceneBase:
    def __init__(self):
        self.next = self
        self.name = "BASE"
        self.song = None

    def process_input(self, events, pressed_keys):
        print("Please override this method in your class.")

    def update(self):
        print("Please override this method in your class.")

    def render(self, screen):
        print("Please override this method in your class.")

    def switch_to_scene(self, next_scene):
        if next_scene is not None and next_scene.song is not None:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(next_scene.song )
            pygame.mixer.music.play(1)
        self.next = next_scene

    def get_next_scene(self):
        next_scene = self.next
        self.next = self
        return next_scene

    def terminate(self):
        self.switch_to_scene(None)


def initialize(width, height):
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    return screen


def run_game(screen, fps, starting_scene):
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.terminate()
            else:
                filtered_events.append(event)

        active_scene.process_input(filtered_events, pressed_keys)
        active_scene.update()
        active_scene.render(screen)
        active_scene = active_scene.get_next_scene()

        pygame.display.flip()
        clock.tick(fps)
