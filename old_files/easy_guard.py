import pygame
from enemy import Enemy
class Easy_Guard(Enemy):
    def __init__(self, direction="Down"):
        super().__init__(self, direction)
        self._state = "Alive"  # alive or dead
        self._direction = direction  # the direction they are facing
        self._left = pygame.image.load("./assets/graphics/Guard_EASY.png")
        self._right = pygame.image.load("./assets/graphics/Guard_EASY.png")
        self._up = pygame.image.load("./assets/graphics/Guard_EASY.png")
        self._down = pygame.image.load("./assets/graphics/Guard_EASY.png")

    @property
    def image(self):
        match self._direction:
            case "left":
                return self._left
            case "right":
                return self._right
            case "up":
                return self._up
            case "down":
                return self._down
