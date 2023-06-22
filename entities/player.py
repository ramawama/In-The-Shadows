import pygame


class Player:
    def __init__(self, screen, x, y, resolution):
        self.__resolution = resolution
        self.__alive = True
        self.__screen = screen
        self.__right = [pygame.transform.scale(pygame.image.load("assets/graphics/Rogue/Rogue.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32)),
                        pygame.transform.scale(pygame.image.load("assets/graphics/Rogue/Rogue_walk.png").convert_alpha(), (self.__resolution * 32, self.__resolution * 32))]
        self.__left = [pygame.transform.flip(self.__right[0], True, False),
                       pygame.transform.flip(self.__right[1], True, False)]
        self.__curr_sprites = self.__right
        self.__direction = "right"
        self.__x = x
        self.__y = y

    def draw(self):
        self.__screen.blit(self.__curr_sprites[0], (self.__x * 32 * self.__resolution, self.__y * 32 * self.__resolution))

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
