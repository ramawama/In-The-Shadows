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
                                temp_Tile = Tile("o", False, x, y)
                                row_array.append(temp_Tile)
                                row_char_array.append(Tile("o", False, x, y, temp_Tile.image, temp_Tile.floor_type))
                            elif char in ['e', '!']:
                                self.__exit_tile = x, y
                                temp_Tile = Tile(char, False, x, y)
                                row_array.append(temp_Tile)
                                row_char_array.append(Tile(char, False, x, y, temp_Tile.image, temp_Tile.floor_type))
                            elif char == 't':
                                temp_Tile = Tile(char, True, x, y)
                                row_array.append(temp_Tile)
                                row_char_array.append(Tile(char, True, x, y, temp_Tile.image, temp_Tile.floor_type))
                            else:
                                temp_Tile = Tile(char, False, x, y)
                                row_array.append(temp_Tile)
                                row_char_array.append(Tile(char, False, x, y, temp_Tile.image, temp_Tile.floor_type))
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

    def replace_tile_with_original(self, x, y, play_music):
        if self.__tiles[x][y].lit:
            self.__tiles[x][y] = Tile(self.__orig_tiles[x][y].type, self.__tiles[x][y].lit, y, x, self.__orig_tiles[x][y].image, self.__orig_tiles[x][y].floor_type)
            self.__tiles[x][y].light()
        else:
            self.__tiles[x][y] = Tile(self.__orig_tiles[x][y].type, self.__tiles[x][y].lit, y, x, self.__orig_tiles[x][y].image, self.__orig_tiles[x][y].floor_type)
            if self.__tiles[x][y].type == 't':
                if play_music:
                    pygame.mixer.Sound.play(
                        pygame.mixer.Sound(Path(__file__).parent / "./assets/sounds/light_torch.mp3"))
                self.__tiles[x][y].light()
        self.torch_check()

    def replace_tile_with_guard(self, x, y, image):
        temp_background = self.__tiles[x][y].floor_type
        if self.__tiles[x][y].lit:
            self.__tiles[x][y] = Tile("g", self.__tiles[x][y].lit, y, x, image, temp_background)
            self.__tiles[x][y].light()
        else:
            self.__tiles[x][y] = Tile("g", self.__tiles[x][y].lit, y, x, image, temp_background)
        self.torch_check()

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
                        scaled_floor = pygame.transform.scale(self.__tiles[row][col].backgroundtile, (tile_width, tile_height))
                    else:
                        scaled_floor = pygame.transform.scale(self.__tiles[row][col].backgroundtile,
                                                              (tile_width, tile_height))
                    self.__screen.background_surface.blit(scaled_floor, (tile_x, tile_y))
                self.__screen.background_surface.blit(scaled_tile, (tile_x, tile_y))

    # Returns array of tiles
    @property
    def tiles(self):
        return self.__tiles

    @property
    def orig_tiles(self):
        return self.__orig_tiles

    def unload(self):
        self.__loaded = False
        self.__tiles = []
        self.__orig_tiles = []

    # pass in more parameters like a list of items a player has to display on the HUD
    def display_hud(self, player, chase):
        self.__screen.background_surface.fill((0, 0, 0), pygame.Rect(0, self.__screen_height,
                                                                     self.__screen_width, 128))
        hud_background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/hud_background.png")
        hud_background = pygame.transform.scale(hud_background, (self.__screen_width, self.__screen_height))
        white = (255, 255, 255)
        text_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf',
                                     int(self.__screen_height * 0.025))
        text_font_bold = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf',
                                     int(self.__screen_height * 0.04))

        if player.dash_cooldown == 0:
            status_text = text_font.render('SPACE TO DASH', True, (255, 255, 255))
        elif player.dash_cooldown == 4:
            status_text = text_font.render('DASH READY!', True, (255, 255, 255))
        else:
            status_text = text_font.render('DASH COOLDOWN: ' + str(player.dash_cooldown), True, (255, 255, 255))
        if player.extinguish:
            status_text = text_font.render('BOTTLE READY!', True, (255, 255, 255))
        if player.smoke:
            status_text = text_font.render('SMOKE EMPLOYED!', True, (255, 255, 255))

        status_rect = status_text.get_rect()
        (status_width, status_height) = (0.015 * self.__screen_width, 1.016 * self.__screen_height)
        status_rect.x, status_rect.y = (status_width, status_height)

        curr_level = text_font_bold.render('LEVEL ' + str(self.__level), True, white)
        curr_level_rect = curr_level.get_rect()
        (curr_level_width, curr_level_height) = (self.__screen_width // 2 - curr_level.get_width() // 2, 0.988 * status_height)
        curr_level_rect.x, curr_level_rect.y = (curr_level_width, curr_level_height)

        info_text = text_font.render('INFO (I)', True, white)
        info_text_rect = info_text.get_rect()
        (info_text_width, info_text_height) = (curr_level_width - 0.12 * self.__screen_width - info_text_rect.width, status_height)
        info_text_rect.x, info_text_rect.y = (info_text_width, info_text_height)

        if not player.key:
            instructions = text_font.render('COLLECT THE KEY AND AVOID CAPTURE!', True, white)
        else:
            if self.__level == 3:
                instructions = text_font.render('COLLECT THE TREASURE!', True, white)
            else:
                instructions = text_font.render('ESCAPE TO THE NEXT LEVEL!', True, white)

        if chase:
            instructions = text_font.render('YOU HAVE BEEN SPOTTED! RUN AWAY!', True, (255, 255, 255))

        instructions_rect = instructions.get_rect()
        (instructions_width, instructions_height) = (self.__screen_width - 0.01 * self.__screen_width - instructions_rect.width, status_height)
        instructions_rect.x, instructions_rect.y = (instructions_width, instructions_height)

        self.__screen.background_surface.blit(hud_background, (0, 0.16 * self.__screen_height))
        self.__screen.background_surface.blit(status_text, status_rect)
        self.__screen.background_surface.blit(curr_level, curr_level_rect)
        self.__screen.background_surface.blit(info_text, info_text_rect)
        self.__screen.background_surface.blit(instructions, instructions_rect)
