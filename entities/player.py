import pygame

class Player():
    def __init__(self, direction="Down"):
        self._state = "Alive"  # alive or dead
        self._direction = direction  # the direction they are facing
        self._left = pygame.image.load("./assets/graphics/Rogue.png")
        self._right = pygame.image.load("./assets/graphics/Rogue.png")
        self._up = pygame.image.load("./assets/graphics/Rogue.png")
        self._down = pygame.image.load("./assets/graphics/Rogue.png")

        # more specific enemy entities will have their view radius and character sprites described
    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, state):
        self._state = state

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

