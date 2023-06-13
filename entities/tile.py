import pygame


class Tile():
    def __init__(self, tile_type="o"):
        self._tile_type = tile_type
        self._image = pygame.image.load("./assets/graphics/" + tile_type + ".png")

    @property
    def image(self):
        return self._image
