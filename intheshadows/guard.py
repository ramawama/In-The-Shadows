import pygame
from intheshadows.board import Board
from pathlib import Path


class Guard:
    def __init__(self, screen, resolution, x, y, path="LR", difficulty="EASY"):
        self.__alive = True
        self.__screen = screen
        self.__resolution = resolution
        match difficulty:
            case "EASY":
                self.__difficulty = 1
            case "MEDIUM":
                self.__difficulty = 2
            case "HARD":
                self.__difficulty = 3
            case _:
                self.__difficulty = 1
        self.__right = [pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_walk_1.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_walk_2.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_walk_3.png"), (self.__resolution * 32, self.__resolution * 32))]
        self.__left = [pygame.transform.flip(self.__right[0], True, False),
                       pygame.transform.flip(self.__right[1], True, False),
                       pygame.transform.flip(self.__right[2], True, False),
                       pygame.transform.flip(self.__right[3], True, False)]
        self.__up = [pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_up.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_up_walk_1.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_up_walk_2.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_up_walk_3.png"), (self.__resolution * 32, self.__resolution * 32))]
        self.__down = [pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_down.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_down_walk_1.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_down_walk_2.png"), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / f"assets/graphics/Guard/Guard_{difficulty}_down_walk_3.png"), (self.__resolution * 32, self.__resolution * 32))]
        self.__curr_sprites = self.__right
        self.__direction = "right"
        self.__x = int(x)
        self.__y = int(y)
        self.__route = path

    def draw(self):
        self.__screen.blit(self.__curr_sprites[0],
                           (self.__x * 32 * self.__resolution, self.__y * 32 * self.__resolution))

    @property
    def difficulty(self):
        return self.__difficulty

    @property
    def route(self):
        return self.__route

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction
        match direction:
            case 'U':
                self.__direction = 'up'
            case 'D':
                self.__direction = 'down'
            case 'R':
                self.__direction = 'right'
            case 'L':
                self.__direction = 'left'
            case _:
                self.__direction = direction

    def moveUp(self):
        self.__direction = "up"
        self.__curr_sprites = self.__up
        self.__y -= 1

    def moveLeft(self):
        self.__direction = "left"
        self.__curr_sprites = self.__left
        self.__x -= 1

    def moveDown(self):
        self.__direction = "down"
        self.__curr_sprites = self.__down
        self.__y += 1

    def moveRight(self):
        self.__direction = "right"
        self.__curr_sprites = self.__right
        self.__x += 1

    def currSprites(self):
        return self.__curr_sprites

    def position(self):
        return self.__x, self.__y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    def update_sprites(self):
        if self.__direction == "right":
            self.__curr_sprites = self.__right
        elif self.__direction == "left":
            self.__curr_sprites = self.__left
        elif self.__direction == "up":
            self.__curr_sprites = self.__up
        elif self.__direction == "down":
            self.__curr_sprites = self.__down