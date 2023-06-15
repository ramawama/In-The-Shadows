import pygame

class Window():
    def __init__(self, width, height):
        self.__screen = pygame.display.set_mode((width, height))
        self.__screen.fill((0, 0, 0))
        pygame.display.flip()
        # Create background surface
        self.__background_surface = pygame.Surface((width, height))
        self.__foreground_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def update(self):
        self.__screen.blit(self.__background_surface, (0, 0))
        self.__screen.blit(self.__foreground_surface, (0, 0))
        pygame.display.update()

    @property
    def background_surface(self):
        return self.__background_surface
    
    @property
    def foreground_surface(self):
        return self.__foreground_surface