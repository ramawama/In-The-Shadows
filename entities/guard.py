import pygame
from entities.sprite import Sprite


class Guard(Sprite):
    def __init__(self, width=32, height=32):
        super().__init__(width, height)
        super().set_image('assets/graphics/Guard/Guard_easy.png')

    @property
    def image(self):
        return super().image
