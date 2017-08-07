import pygame

_loaded_images = {}


def load_image(path):
    global _loaded_images
    if path not in _loaded_images:
        image = pygame.image.load(path).convert_alpha()
        _loaded_images[path] = image
    else:
        image = _loaded_images[path]
    return image
