import pygame
from pathlib import Path


class Player:
    def __init__(self, screen, x, y, resolution):
        self.__resolution = resolution
        self.__alive = True
        self.__screen = screen
        self.__right = [pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_walk_1.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_walk_2.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_walk_3.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32))]
        self.__left = [pygame.transform.flip(self.__right[0], True, False),
                       pygame.transform.flip(self.__right[1], True, False),
                       pygame.transform.flip(self.__right[2], True, False),
                       pygame.transform.flip(self.__right[3], True, False)]
        self.__curr_sprites = self.__right
        self.__direction = "right"
        self.__x = x
        self.__y = y
        self.__items = []
        self.__key = False

    def draw(self):
        self.__screen.blit(self.__curr_sprites[0], (self.__x * 32 * self.__resolution, self.__y * 32 * self.__resolution))

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    def moveUp(self):
        if self.__direction == "right":
            self.__curr_sprites = self.__right
        else:
            self.__curr_sprites = self.__left
        self.__y -= 1

    def moveLeft(self):
        self.__direction = "left"
        self.__curr_sprites = self.__left
        self.__x -= 1

    def moveDown(self):
        if self.__direction == "right":
            self.__curr_sprites = self.__right
        else:
            self.__curr_sprites = self.__left
        self.__y += 1

    def moveRight(self):
        self.__direction = "right"
        self.__curr_sprites = self.__right
        self.__x += 1

    def currSprites(self):
        if self.__direction == "right":
            self.__curr_sprites = self.__right
        else:
            self.__curr_sprites = self.__left
        return self.__curr_sprites

    def position(self):
        return self.__x, self.__y

    #add item to inventory
    def add_item(self, item):
        self.__items.append(item)
