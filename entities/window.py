import pygame


# Class for the main window and corresponding surfaces (background and foreground)
class Window:
    def __init__(self, width, height):
        self.__screen = pygame.display.set_mode((width, height))
        self.__screen.fill((0, 0, 0))
        pygame.display.flip()

        # Create surfaces
        self.__background_surface = pygame.Surface((width, height))
        self.__foreground_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Refresh all display elements every cycle
    def update(self):
        self.__screen.blit(self.__background_surface, (0, 0))
        self.__screen.blit(self.__foreground_surface, (0, 0))
        pygame.display.update()

    def resize(self, width, height):
        self.__screen = pygame.display.set_mode((width, height))
        self.__background_surface = pygame.Surface((width, height))
        self.__foreground_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Returns background surface
    @property
    def background_surface(self):
        return self.__background_surface

    # Returns foreground surface
    @property
    def foreground_surface(self):
        return self.__foreground_surface
