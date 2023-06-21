import pygame


class Tile:
    def __init__(self, tile_type="o", behind_torch=False, x=0, y=0):
        self._tile_type = tile_type
        self._pos = [x, y]
        self._lit = False
        self.unlight()
        self.__torch_counter = 0
        if behind_torch is False:
            self._backgroundtile = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor.png")
        else:
            self._backgroundtile = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor_lit.png")
        match tile_type:
            case "t":
                self.light()
            case "g":
                self._image = pygame.image.load("./assets/graphics/Guard/Guard_easy.png")
            case "p":
                self._image = pygame.image.load("./assets/graphics/Rogue/Rogue.png")
            case "w":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_t.png")
            case "m":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_b.png")
            case "l":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_l.png")
            case "r":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_r.png")
            case "1":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_corner_tl.png")
            case "2":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_corner_tr.png")
            case "3":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_corner_bl.png")
            case "4":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall_corner_br.png")
            case "e":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Exit.png")
            case "k":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Key.png")

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

    # Sets a tile as lit
    def light(self):
        self._lit = True
        if self.type == "o":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor_lit.png")
        elif self.type == "t":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Torch/Torch_small.png")

    def unlight(self):
        self._lit = False
        if self.type == "o":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor.png")
        elif self.type == "t":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Torch/Torch_unlit.png")
