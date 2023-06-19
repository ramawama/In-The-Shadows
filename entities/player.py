import pygame
from entities.board import Board


class Player:
    def __init__(self, screen, x, y):
        self.__alive = True
        self.__screen = screen
        self.__right = [pygame.image.load("assets/graphics/Rogue/Rogue.png"),
                        pygame.image.load("assets/graphics/Rogue/Rogue_walk.png")]
        self.__left = [pygame.transform.flip(self.__right[0], True, False),
                       pygame.transform.flip(self.__right[1], True, False)]
        self.__curr_sprites = self.__right
        self.__direction = "right"
        self.__x = x
        self.__y = y

    def draw(self):
        self.__screen.blit(self.__curr_sprites[0], (self.__x, self.__y))

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction

    def moveUp(self):
        pass

    def moveLeft(self):
        pass

    def moveDown(self):
        pass

    def moveRight(self):
        self.__direction = "right"
        self.__curr_sprites = self.__right
        self.__x += 32


