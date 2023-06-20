import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.__width = width
        self.__height = height
        self.__image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.__image.fill((255, 255, 255))
        pygame.draw.rect(self.__image, (255, 255, 255), pygame.Rect(0, 0, width, height))
        self.__rect = self.__image.get_rect()

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    def set_image(self, image):
        self.__image.fill((0, 0, 0, 0))
        self.__image.blit(pygame.transform.scale(pygame.image.load(image), (self.__width, self.__height)),
                          (0, 0))
