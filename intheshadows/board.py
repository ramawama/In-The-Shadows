import copy
from pathlib import Path
import pygame
from intheshadows.tile import Tile


# Class for the game board (collection of all tiles)
class Board:
    def __init__(self, screen, width, height):
        self.__resolution = width // 896
        self.__orig_tiles = []
        self.__tiles = []
        self.__screen = screen
        self.__loaded = False
        self.__screen_width = width
        self.__screen_height = height - (32 * self.__resolution)
        self.__level = 1
        self.__exit_tile = [0, 0]

    def unlock(self):
        self.__tiles[self.__exit_tile[1]][self.__exit_tile[0]].unlock()

    def resize_board(self, screen, width, height):
        self.__resolution = width // 896
        self.__screen = screen
        self.__screen_width = width
        self.__screen_height = height - (32 * self.__resolution)

    # Load the level from a file
    def load_level(self, name=1):
        if not self.__loaded:
            try:
                self.__level = name
                with open(Path(__file__).parent / ('levels/level_' + str(name)), 'r') as file:
                    file.readline().strip()
                    lines = file.readlines()
                    file.close()
                    x = 0
                    y = 0
                    playerPos = [0, 0]
                    line_counter = 0
                    guards = []
                    for line in lines:
                        line_counter = line_counter + 1
                        if line.strip() == "END":
                            break
                        row_array = []
                        row_char_array = []
                        for char in line.strip():
                            if char == "p":
                                playerPos = [x, y]
                                row_array.append(Tile("o", False, x, y))
                                row_char_array.append("o")
                            elif char in ['e', 'c']:
                                self.__exit_tile = x, y
                                row_array.append(Tile(char, False, x, y))
                                row_char_array.append(char)
                            else:
                                row_array.append(Tile(char, False, x, y))
                                row_char_array.append(char)
                            # if char == "g":
                            # print("guard at: x:", x, " y: ", y)
                            # if char == "p":
                            # print("spawn at at: x:", x, " y: ", y)
                            x += 1
                        self.__tiles.append(row_array)
                        self.__orig_tiles.append(row_char_array)
                        y += 1
                        x = 0
                for x in range(line_counter, len(lines), 2):
                    guards.append((lines[x].strip().split(), lines[x + 1].strip()))
                #  Update torch count for all tiles
                self.torch_check()
                self.__loaded = True
                return playerPos, guards
            except IOError:
                print("Error from load_tiles function!")

    def replace_tile_with_original(self, x, y):
        self.__tiles[x][y] = Tile(self.__orig_tiles[x][y], self.__tiles[x][y].lit, x, y)
        self.torch_check()

    def replace_tile_with_guard(self, x, y, image):
        self.__tiles[x][y] = Tile("g", self.__tiles[x][y].lit, x, y, image)

    def check_for_key(self):
        for row in range(len(self.__tiles)):
            for col in range(len(self.__tiles[row])):
                if self.__tiles[row][col].type == "k":
                    return True
        return False

    # Illuminates tiles near torches
    def torch_check(self):
        surrounding_tiles = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        for row in range(len(self.__tiles)):
            for col in range(len(self.__tiles[row])):
                if self.__tiles[row][col].type == "t":
                    if self.__tiles[row][col].lit is True:
                        for neighbor in surrounding_tiles:
                            try:
                                self.__tiles[row + neighbor[0]][col + neighbor[1]].light()
                            except IndexError:
                                pass
                    else:
                        for neighbor in surrounding_tiles:
                            try:
                                self.__tiles[row + neighbor[0]][col + neighbor[1]].unlight()
                            except IndexError:
                                pass

    # Draws tiles on background_surface
    def draw_level(self):
        self.__screen.background_surface.fill((0, 0, 0), pygame.Rect(0, 0, self.__screen_width, self.__screen_height))
        self.__screen.foreground_surface.fill((0, 0, 0, 0))
        rows = len(self.__tiles)
        cols = len(self.__tiles[0])

        tile_width = self.__screen_width // cols
        tile_height = self.__screen_height // rows

        for row in range(rows):
            for col in range(cols):
                tile_x = col * tile_width
                tile_y = row * tile_height
                scaled_tile = pygame.transform.scale(self.__tiles[row][col].image, (tile_width, tile_height))
                if self.__tiles[row][col].type != "o":
                    if self.__tiles[row][col].lit:
                        scaled_floor = pygame.transform.scale(Tile("o", True).backgroundtile, (tile_width, tile_height))
                    else:
                        scaled_floor = pygame.transform.scale(self.__tiles[row][col].backgroundtile,
                                                              (tile_width, tile_height))
                    self.__screen.background_surface.blit(scaled_floor, (tile_x, tile_y))
                self.__screen.foreground_surface.blit(scaled_tile, (tile_x, tile_y))

    # Returns array of tiles
    @property
    def tiles(self):
        return self.__tiles

    def unload(self):
        self.__loaded = False
        self.__tiles = []
        self.__orig_tiles = []

    # pass in more parameters like a list of items a player has to display on the HUD
    def display_hud(self, key=False):
        self.__screen.background_surface.fill((0, 0, 0), pygame.Rect(0, self.__screen_height,
                                                                     self.__screen_width, 128))
        white = (255, 255, 255)
        text_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Digital.TTF', int(self.__screen_height * 0.04))
        help_text = text_font.render('H FOR HELP:', True, white)
        help_rect = help_text.get_rect()
        (help_width, help_height) = (self.__screen_width // (10 * self.__resolution),
                                     self.__screen_height + (16 * self.__resolution))
        help_rect.center = (help_width, help_height)

        curr_level = text_font.render('LEVEL ' + str(self.__level), True, white)
        curr_level_rect = curr_level.get_rect()
        (curr_level_width, curr_level_height) = (self.__screen_width // 2 - 32, help_height)
        curr_level_rect.center = (curr_level_width, curr_level_height)

        if not key:
            instructions = text_font.render('COLLECT THE KEY AND AVOID CAPTURE!', True, white)
        else:
            if self.__level == 3:
                instructions = text_font.render('KEY COLLECTED! COLLECT THE TREASURE', True, white)
            else:
                instructions = text_font.render('KEY COLLECTED! ESCAPE TO THE NEXT LEVEL', True, white)

        instructions_rect = instructions.get_rect()
        (instructions_width, instructions_height) = (curr_level_width + (256 * self.__resolution), help_height)
        instructions_rect.center = (instructions_width, instructions_height)

        self.__screen.background_surface.blit(help_text, help_rect)
        self.__screen.background_surface.blit(curr_level, curr_level_rect)
        self.__screen.background_surface.blit(instructions, instructions_rect)
