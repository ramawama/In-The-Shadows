import pygame
from entities.tile import Tile


# Class for the game board (collection of all tiles)
class Board:
    def __init__(self, screen, width, height):
        self.__tiles = []
        self.__screen = screen
        self.__loaded = False
        self.__screen_width = width
        self.__screen_height = height - 32
        self.__resolution = width // 896

    def resize_board(self, screen, width, height):
        self.__resolution = width // 896
        self.__screen = screen
        self.__screen_width = width
        self.__screen_height = height - (32 * self.__resolution)

    # Load the level from a file
    def load_level(self, name=1):
        if not self.__loaded:
            try:
                with open('./levels/level_' + str(name), 'r') as file:
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
                        for char in line.strip():
                            if char == "p":
                                playerPos = [x, y]
                                row_array.append(Tile("o", False, x, y))
                            else:
                                row_array.append(Tile(char, False, x, y))
                            # if char == "g":
                            # print("guard at: x:", x, " y: ", y)
                            # if char == "p":
                            # print("spawn at at: x:", x, " y: ", y)
                            x += 1
                        self.__tiles.append(row_array)
                        y += 1
                        x = 0
                for x in range(line_counter, len(lines), 3):
                    guards.append((lines[x].strip(), lines[x+1].strip().split(), lines[x+2].strip()))
                #  Update torch count for all tiles
                self.torch_check()
                self.__loaded = True
                return playerPos, guards
            except IOError:
                print("Error from load_tiles function!")

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
        self.__screen.background_surface.fill((0, 0, 0))
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
        self.display_hud()

    # Returns array of tiles
    @property
    def tiles(self):
        return self.__tiles

    def unload(self):
        self.__loaded = False
        self.__tiles = []

    # pass in more parameters like a list of items a player has to display on the HUD
    def display_hud(self):
        white = (255, 255, 255)
        text_font = pygame.font.Font('assets/fonts/Digital.TTF', int(self.__screen_height * 0.04))
        instructions_text = text_font.render('MOVE:', True, white)
        instructions_rect = instructions_text.get_rect()
        (instruct_width, instruct_height) = (self.__screen_width // (16 * self.__resolution),
                                             self.__screen_height + (16 * self.__resolution))
        instructions_rect.center = (instruct_width, instruct_height)

        movement_up = text_font.render('↑', True, white)
        movement_up_rect = movement_up.get_rect()
        (movement_up_width, movement_up_height) = (instruct_width + (32 * self.__resolution),
                                                   instruct_height - (16 * self.__resolution))
        movement_up_rect.center = (movement_up_width, movement_up_height)

        movement = text_font.render('← ↓ →', True, white)
        movement_rect = movement.get_rect()
        (movement_width, movement_height) = (movement_up_width + (32 * self.__resolution), instruct_height + (10 * self.__resolution))
        movement_rect.center = (movement_width, movement_height)

        self.__screen.background_surface.blit(instructions_text, instructions_rect)
        self.__screen.background_surface.blit(movement_up, movement_up_rect)
        self.__screen.background_surface.blit(movement, movement_rect)

        self.__screen.background_surface.blit(instructions_text, instructions_rect)

