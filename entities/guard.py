import pygame
from entities.board import Board


class Guard:
    def __init__(self, screen, resolution, x, y, path="", difficulty="easy", width=32, height=32):
        self.__alive = True
        self.__screen = screen
        self.__resolution = resolution
        match difficulty:
            case "easy":
                self.__difficulty = 1
            case "med":
                self.__difficulty = 2
            case "hard":
                self.__difficulty = 3
            case other:
                self.__difficulty = 1
        self.__right = [pygame.transform.scale(pygame.image.load(f"assets/graphics/Guard/Guard_{difficulty}.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(f"assets/graphics/Guard/Guard_{difficulty}_walk.png"), (self.__resolution * 32, self.__resolution * 32))]
        self.__left = [pygame.transform.flip(self.__right[0], True, False),
                       pygame.transform.flip(self.__right[1], True, False)]
        self.__curr_sprites = self.__right
        self.__direction = "right"
        self.__x = int(x)
        self.__y = int(y)

    def draw(self):
        self.__screen.blit(self.__curr_sprites[0],
                           (self.__x * 32 * self.__resolution, self.__y * 32 * self.__resolution))

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


