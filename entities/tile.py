import pygame


class Tile:
    def __init__(self, tile_type="o", behind_torch=False, x=0, y=0):
        self._tile_type = tile_type
        self._pos = [x, y]
        self._lit = False
        self.unlight()
        self.__torch_counter = 0
        if behind_torch is False:
            self._backgroundtile = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor.png").convert_alpha()
        else:
            self._backgroundtile = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor_lit.png").convert_alpha()
        match tile_type:
            case "t":
                self.light()
            case "g":
                self._image = pygame.image.load("./assets/graphics/Guard/Guard_easy.png").convert_alpha()
            case "p":
                self._image = pygame.image.load("./assets/graphics/Rogue/Rogue.png").convert_alpha()
            case "w":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_t.png").convert_alpha()
            case "m":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_b.png").convert_alpha()
            case "l":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_l.png").convert_alpha()
            case "r":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_r.png").convert_alpha()
            case "1":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_corner_tl.png").convert_alpha()
            case "2":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_corner_tr.png").convert_alpha()
            case "3":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_corner_bl.png").convert_alpha()
            case "4":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_corner_br.png").convert_alpha()
            case "e":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Exit.png").convert_alpha()
            case "k":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Key.png").convert_alpha()

    @property
    def image(self):
        return self._image

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

    # Sets a tile as lit
    def light(self):
        self._lit = True
        if self.type == "o":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor_lit.png").convert_alpha()
        elif self.type == "t":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Torch/Torch_small.png").convert_alpha()

    def unlight(self):
        self._lit = False
        if self.type == "o":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor.png").convert_alpha()
        elif self.type == "t":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Torch/Torch_unlit.png").convert_alpha()
