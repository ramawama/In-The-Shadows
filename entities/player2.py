import pygame
from entities.sprite import Sprite


class Player(Sprite):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.__right = "assets/graphics/Rogue/Rogue.png"
        self.__rightWalk = "assets/graphics/Rogue/Rogue_walk.png"
        super().set_image(self.__right)
        self.__direction = "right"

    def moveDown(self):
        super().set_image(self.__rightWalk)
        super().rect.y += 32
