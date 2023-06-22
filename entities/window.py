import pygame


# Class for the main window and corresponding surfaces (background and foreground)
class Window:
    def __init__(self, width, height):
        self.__screen = pygame.display.set_mode((width, height))
        self.__screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.display.set_caption("In The Shadows")
        pygame.display.set_icon(pygame.image.load("./assets/graphics/Rogue/Rogue_walk_2.png").convert_alpha())

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
        self.__background_surface = pygame.transform.scale(self.__background_surface, (width, height))
        self.__foreground_surface = pygame.transform.scale(self.__foreground_surface, (width, height))

    # Returns background surface
    @property
    def background_surface(self):
        return self.__background_surface

    # Returns foreground surface
    @property
    def foreground_surface(self):
        return self.__foreground_surface
