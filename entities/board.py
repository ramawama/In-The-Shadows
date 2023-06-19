import pygame
from entities.tile import Tile


# Class for the game board (collection of all tiles)
class Board:
    def __init__(self, screen, width, height):
        self.__tiles = []
        self.__screen = screen
        self.__loaded = False
        self.__screen_width = width
        self.__screen_height = height

    # Load the level from a file
    def load_level(self, name="level_TEST"):
        if not self.__loaded:
            try:
                with open('./levels/' + name, 'r') as file:
                    file.readline().strip()
                    lines = file.readlines()
                    file.close()
                    x = 0
                    y = 0
                    playerPos = [0, 0]
                    for line in lines:
                        if line.strip() == "END":
                            break
                        row_array = []
                        for char in line.strip():
                            row_array.append(Tile(char, False, x, y))
                            if char == "p":
                                playerPos = [x, y]
                            x += 1
                        self.__tiles.append(row_array)
                        y += 1
                        x = 0
                self.__torch_check()
                self.__loaded = True
                return playerPos
            except IOError:
                print("Error from load_tiles function!")

    # Illuminates tiles near torches
    def __torch_check(self):
        for row in range(len(self.__tiles)):
            for col in range(len(self.__tiles[row])):
                if self.__tiles[row][col].type == "t":
                    self.__tiles[row + 1][col].light()
                    self.__tiles[row + 1][col - 1].light()
                    self.__tiles[row + 1][col + 1].light()
                    self.__tiles[row - 1][col].light()
                    self.__tiles[row - 1][col - 1].light()
                    self.__tiles[row - 1][col + 1].light()
                    self.__tiles[row][col - 1].light()
                    self.__tiles[row][col + 1].light()

    # Draws tiles on background_surface
    def draw_level(self):
        self.__screen.background_surface.fill((0, 0, 0))
        self.__screen.foreground_surface.fill((0, 0, 0, 0))

        rows = len(self.__tiles)
        cols = len(self.__tiles[0])

        tile_width = self.__screen_width / cols
        tile_height = self.__screen_height / rows

        for row in range(rows):
            for col in range(cols):
                tile_x = col * tile_width
                tile_y = row * tile_height

                scaled_tile = pygame.transform.scale(self.__tiles[row][col].image, (tile_width, tile_height))
                if self.__tiles[row][col].type != "o":
                    if self.__tiles[row][col].lit:
                        scaled_floor = pygame.transform.scale(Tile("o", True).image, (tile_width, tile_height))
                    else:
                        scaled_floor = pygame.transform.scale(Tile().image, (tile_width, tile_height))
                    self.__screen.background_surface.blit(scaled_floor, (tile_x, tile_y))
                self.__screen.foreground_surface.blit(scaled_tile, (tile_x, tile_y))

    # Returns array of tiles
    @property
    def tiles(self):
        return self.__tiles
