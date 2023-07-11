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
        self.__up = [pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_up.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                    pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_up_walk_1.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                    pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_up_walk_2.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                    pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_up_walk_3.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32))]
        self.__down = [pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_fwd.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                    pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_fwd_walk_1.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                    pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_fwd_walk_2.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                    pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue_fwd_walk_3.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32))]
        self.__curr_sprites = self.__right
        self.__direction = "right"
        self.__x = x
        self.__y = y
        self.__items = []
        self.__key = False
        self.__dash = False

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

    @property
    def dash(self):
        return self.__dash

    @dash.setter
    def dash(self, dash):
        self.__dash = dash

    @key.setter
    def key(self, key):
        self.__key = key

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

    # add item to inventory
    def add_item(self, item):
        self.__items.append(item)

