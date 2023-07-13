import pygame
from pathlib import Path
import random


class Tile:
    def __init__(self, tile_type="o", behind_torch=False, x=0, y=0, image=None, floor_type=""):
        self._tile_type = tile_type
        self._pos = [x, y]
        self._lit = False
        self._behind_torch = behind_torch
        #self.unlight()
        self.__torch_counter = 0
        self._image = image
        self._floor_type = floor_type
        random_selector = random.randint(0, 4)
        rand_int = random.randint(2, 4)
        if image is None:
            match tile_type:
                case "t":
                    self.light()
                case "g":
                    self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Guard/Guard_EASY.png").convert_alpha()
                case "p":
                    self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Rogue/Rogue.png").convert_alpha()
                case "w":
                    if x == 0 and y == 0:
                        self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Wall_corner_tl.png").convert_alpha()
                    elif x == 0 and y == 14:
                        self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Wall_corner_bl.png").convert_alpha()
                    elif x == 27 and y == 0:
                        self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Wall_corner_tr.png").convert_alpha()
                    elif x == 27 and y == 14:
                        self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Wall_corner_br.png").convert_alpha()
                    elif y == 0:
                        self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Wall_t.png").convert_alpha()
                    elif x == 0:
                        self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Wall_l.png").convert_alpha()
                    elif x == 27:
                        self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Wall_r.png").convert_alpha()
                    elif y == 14:
                        self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Wall_b.png").convert_alpha()
                    else:
                        self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Wall_t.png").convert_alpha()
                case "e":
                    self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Exit_locked.png").convert_alpha()
                case "k":
                    self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Key.png").convert_alpha()
                case "c":
                    self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Chest_locked.png").convert_alpha()
                case "o":
                    if random_selector == 0:
                        match rand_int:
                            case 2:
                                self._floor_type = "_cracked"
                            case 3:
                                self._floor_type = "_cracked_mossy"
                            case 4:
                                self._floor_type = "_mossy"
                        # print(("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + ".png"))
                    self._image = pygame.image.load(Path(__file__).parent / ("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + ".png")).convert_alpha()
        if behind_torch is False:
            #print(("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + ".png"))
            self._backgroundtile = pygame.image.load(Path(__file__).parent / ("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + ".png")).convert_alpha()
        else:
            #print(("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + ".png"))
            self._backgroundtile = pygame.image.load(Path(__file__).parent / ("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + "_lit.png")).convert_alpha()
    @property
    def image(self):
        return self._image

    @property
    def behind_torch(self):
        return self._behind_torch

    @property
    def floor_type(self):
        return self._floor_type

    @property
    def type(self):
        return self._tile_type

    @property
    def lit(self):
        return self._lit

    @property
    def pos(self):
        return self._pos

    @property
    def backgroundtile(self):
        return self._backgroundtile

    @backgroundtile.setter
    def backgroundtile(self, backgroundtile):
        self._backgroundtile = backgroundtile

    # Sets a tile as lit
    def light(self):
        self._lit = True
        if self.type == "o":
            self._image = pygame.image.load(Path(__file__).parent / ("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + "_lit.png")).convert_alpha()
        elif self.type == "t":
            self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Torch/Torch_small.png").convert_alpha()
            self._backgroundtile = pygame.image.load(Path(__file__).parent / ("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + "_lit.png")).convert_alpha()
        elif self.type == 'g':
            self._backgroundtile = pygame.image.load(Path(__file__).parent / ("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + "_lit.png")).convert_alpha()

    def unlight(self):
        self._lit = False
        if self.type == "o":
            self._image = pygame.image.load(Path(__file__).parent / ("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + ".png")).convert_alpha()
        elif self.type == "t":
            self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Torch/Torch_unlit.png").convert_alpha()
            self._backgroundtile = pygame.image.load(Path(__file__).parent / ("assets/graphics/Level Elements/Floor/Floor" + self._floor_type + ".png")).convert_alpha()

    def unlock(self):
        if self.type == "e":
            self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Exit.png").convert_alpha()
        elif self.type == 'c':
            self._image = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Chest.png").convert_alpha()
