import pygame


class Tile:
    def __init__(self, tile_type="o", behind_torch=False, x=0, y=0):
        self._tile_type = tile_type
        self._pos = [x, y]
        match tile_type:
            case "t":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Torch/Torch_small.png")
            case "o":
                if behind_torch:
                    self.light()
                else:
                    self._image = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor.png")
            case "g":
                self._image = pygame.image.load("./assets/graphics/Guard/Guard_easy.png")
            case "p":
                self._image = pygame.image.load("./assets/graphics/Rogue/Rogue.png")
            case "w":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Wall.png")
            case "e":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Exit.png")
            case "k":
                self._image = pygame.image.load("./assets/graphics/Level Elements/Key.png")

        if tile_type == "t":
            self._lit = True
        else:
            self._lit = False

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

    def unlight(self):
        self._lit = False
        if self.type == "o":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Floor/Floor.png")
        if self.type == "t":
            self._image = pygame.image.load("./assets/graphics/Level Elements/Torch/Torch_unlit.png")
