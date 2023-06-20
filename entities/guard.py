import pygame
from entities.board import Board


class Guard:
    def __init__(self, screen, x, y, width, height, difficulty):
        self.__alive = True
        self.__screen = screen
        self.__difficulty = difficulty
        self.__right = [pygame.transform.scale(pygame.image.load(f"assets/graphics/Guard/Guard_{difficulty}.png"), (width / 28, height // 15)),
                        pygame.transform.scale(pygame.image.load(f"assets/graphics/Guard/Guard_{difficulty}_walk.png"), (width / 28, height // 15))]
        self.__left = [pygame.transform.flip(self.__right[0], True, False),
                       pygame.transform.flip(self.__right[1], True, False)]
        self.__curr_sprites = self.__right
        self.__direction = "right"
        self.__x = x
        self.__y = y

    def draw(self):
        self.__screen.blit(self.__curr_sprites[0], (self.__x * 32, self.__y * 32))

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction

    def moveUp(self):
        if self.__direction == "right":
            self.__curr_sprites = self.__right
        else:
            self.__curr_sprites = self.__left
        self.__y -= 1 * self.__difficulty

    def moveLeft(self):
        self.__direction = "left"
        self.__curr_sprites = self.__left
        self.__x -= 1 * self.__difficulty

    def moveDown(self):
        if self.__direction == "right":
            self.__curr_sprites = self.__right
        else:
            self.__curr_sprites = self.__left
        self.__y += 1 * self.__difficulty

    def moveRight(self):
        self.__direction = "right"
        self.__curr_sprites = self.__right
        self.__x += 1 * self.__difficulty

    def currSprites(self):
        if self.__direction == "right":
            self.__curr_sprites = self.__right
        else:
            self.__curr_sprites = self.__left
        return self.__curr_sprites

    def position(self):
        return self.__x, self.__y


