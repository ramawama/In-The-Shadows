import pygame


class Tile():
    def __init__(self, tile_type="o"):
        self._tile_type = tile_type
        self._image = pygame.image.load("./assets/graphics/" + tile_type + ".png")
        if tile_type == "t":
            self._lit = True
        else:
            self._lit = False

    @property
    def image(self):
        return self._image

    @property
    def type(self):
        return self._tile_type

    def light(self):
        self._lit = True
        self._image = pygame.image.load("./assets/graphics/" + self._tile_type + "_lit.png")