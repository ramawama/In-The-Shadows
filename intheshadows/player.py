import pygame
from pathlib import Path


class Player:
    def __init__(self, screen, x, y, resolution):
        self.__extinguish = False
        self.__smoke = False
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
        self.__dash_sprites = [self.__curr_sprites[0], self.__curr_sprites[1], self.__curr_sprites[2], self.__curr_sprites[2], self.__curr_sprites[2], self.__curr_sprites[2], self.__curr_sprites[2], self.__curr_sprites[3]]
        self.__direction = "right"
        self.__dash_cooldown = 0
        self.__x = x
        self.__y = y
        self.__items = []
        self.__key = False
        self.__dash = False

    def draw(self):
        self.__screen.blit(self.__curr_sprites[0], (self.__x * 32 * self.__resolution, self.__y * 32 * self.__resolution))

    @property
    def dash(self):
        return self.__dash

    @dash.setter
    def dash(self, dash):
        self.__dash = dash

    @property
    def dash_cooldown(self):
        return self.__dash_cooldown

    @dash_cooldown.setter
    def dash_cooldown(self, dash_cooldown):
        self.__dash_cooldown = dash_cooldown

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
    def smoke(self):
        return self.__smoke

    @smoke.setter
    def smoke(self, smoke):
        self.__smoke = smoke

    @property
    def extinguish(self):
        return self.__extinguish

    @extinguish.setter
    def extinguish(self, extinguish):
        self.__extinguish = extinguish

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

    def update_sprites(self):
        if self.__direction == "right":
            self.__curr_sprites = self.__right
        elif self.__direction == "left":
            self.__curr_sprites = self.__left
        elif self.__direction == "up":
            self.__curr_sprites = self.__up
        elif self.__direction == "down":
            self.__curr_sprites = self.__down
        if self.__dash:
            self.__curr_sprites = self.update_dash_sprites()


    def update_dash_sprites(self):
        self.__dash_sprites = [self.__curr_sprites[0], self.__curr_sprites[1], self.__curr_sprites[2], self.__curr_sprites[2],
                       self.__curr_sprites[2], self.__curr_sprites[2], self.__curr_sprites[2], self.__curr_sprites[3]]
        return self.__dash_sprites

