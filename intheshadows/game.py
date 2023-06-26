import queue
import time
from pathlib import Path
import pygame
import os
from intheshadows.print import display_help, run_menu, run_options
from intheshadows.events import game_over, win
from intheshadows.guard import Guard
from intheshadows.tile import Tile
from intheshadows.window import Window
from intheshadows.music import Music
from intheshadows.board import Board
from intheshadows.player import Player


class Game:
    def __init__(self):
        # Create global variables for height, width, and black and white colors
        self.__move_flag = None
        self.__anim_counter = None
        self.__black = (0, 0, 0)
        self.__white = (255, 255, 255)
        (self.__width, self.__height) = (64*28, 64*16)

        self.__level = 1
        self.__torch_counter = 0
        self.__move_counter = 0
        self.__move_direction = 'right'
        self.__anim_torches = True
        self.__guard_tracking = False

        self.__resolution = 2  # resolution option for scaling

        # Create window
        self.__screen = Window(self.__width, self.__height)

        # Set Initial State
        self.__state = 'menu'

        self.__rects = {}

        # Initialize Fonts
        pygame.font.init()

        # Create global variable for program status
        self.__running = True

        # Initialize Music
        self.__music = Music()

        # Initialize Board Class
        self.__board = Board(self.__screen, self.__width, self.__height)

        # Load difficulty
        self.__difficulty = "EASY"
        self.__guard_difficulty = 1

        self.__position = ()
        self.__guard_positions = []

        self.__player_spawn, self.__guard_routes = self.__get_spawns()

        self.__set_player_and_guards()

        self.__fullscreen = True

    def __set_player_and_guards(self):
        self.__player = Player(self.__screen.foreground_surface, self.__player_spawn[0], self.__player_spawn[1],
                               self.__resolution)
        self.__guards = []
        self.__guard_positions.clear()
        for x in range(len(self.__guard_routes)):
            self.__guards.append(Guard(self.__screen.foreground_surface, self.__resolution, self.__guard_routes[x][0][0],
                                       self.__guard_routes[x][0][1], self.__guard_routes[x][1],
                                       self.__difficulty))
            self.__guard_positions.append(())
        self.__turn_counter = 0

    # Changes states when escape is pressed
    def __escape_state(self):
        match self.__state:
            case 'options':
                self.__state = 'menu'
            case 'game':
                self.__state = 'menu'
                self.__set_player_and_guards()
            case 'menu':
                self.__running = False
            case 'game_over':
                self.__state = 'menu'
            case 'win':
                self.__state = 'menu'
            case 'help':
                self.__state = 'game'

    # Changes state based on button click
    def __mouse_click(self, mouse_pos):
        if self.__state == 'menu':
            if self.__rects['start_text_rect'].collidepoint(mouse_pos):
                self.__state = 'game'
                self.__board.unload()
                self.__player_spawn, self.__guard_routes = self.__load_game()
                self.__set_player_and_guards()
            elif self.__rects['options_text_rect'].collidepoint(mouse_pos):
                self.__state = 'options'
            elif self.__rects['quit_text_rect'].collidepoint(mouse_pos):
                self.__running = False
        elif self.__state == 'options':
            if self.__rects['easy_difficulty_rect'].collidepoint(mouse_pos):
                self.__difficulty = "EASY"
                self.__guard_difficulty = 1
            elif self.__rects['medium_difficulty_rect'].collidepoint(mouse_pos):
                self.__difficulty = "MEDIUM"
                self.__guard_difficulty = 2
            elif self.__rects['hard_difficulty_rect'].collidepoint(mouse_pos):
                self.__difficulty = "HARD"
                self.__guard_difficulty = 3
            elif self.__rects['resolution_def_rect'].collidepoint(mouse_pos):
                if self.__fullscreen:
                    (self.__width, self.__height) = (32 * 28, 32 * 16)
                    self.__resolution = 1
                    self.__screen.resize(self.__width, self.__height)
                    self.__board.resize_board(self.__screen, self.__width, self.__height)
                    self.__set_player_and_guards()
                    pygame.display.toggle_fullscreen()
                    self.__fullscreen = False
            elif self.__rects['resolution_2_rect'].collidepoint(mouse_pos):
                if not self.__fullscreen:
                    (self.__width, self.__height) = (64 * 28, 64 * 16)
                    self.__resolution = 2
                    self.__screen.resize(self.__width, self.__height)
                    self.__board.resize_board(self.__screen, self.__width, self.__height)
                    self.__set_player_and_guards()
                    self.__fullscreen = True
            elif self.__rects['options_back_button'].collidepoint(mouse_pos):
                self.__state = 'menu'

    # Handles quitting, key presses, and mouse clicks, including in game
    def __handle_events(self):
        if self.__state == 'game':
            for ev in pygame.event.get():
                match ev.type:
                    case pygame.QUIT:
                        self.__running = False
                    case pygame.KEYDOWN:
                        match ev.key:
                            case pygame.K_h: # help screen in game
                                self.__state = 'help'
                            case pygame.K_m:
                                self.__music.toggle()
                            case pygame.K_k:
                                self.__guard_tracking = not self.__guard_tracking
                            case pygame.K_ESCAPE:
                                self.__escape_state()
                            case pygame.K_w | pygame.K_UP:
                                if self.__allow_movement is False:
                                    continue
                                self.__allow_movement = False
                                self.__state = 'move'
                                self.__move_direction = 'up'
                                self.__move_counter = 0
                                self.__anim_counter = 0
                                self.__position = (self.__player.position()[0] * 32 * self.__resolution,
                                                   self.__player.position()[1] * 32 * self.__resolution)
                                for x in range(len(self.__guards)):
                                    self.__guard_positions[x] = (self.__guards[x].position()[0] * 32 * self.__resolution,
                                                       self.__guards[x].position()[1] * 32 * self.__resolution)
                            case pygame.K_a | pygame.K_LEFT:
                                if self.__allow_movement is False:
                                    continue
                                self.__allow_movement = False
                                self.__state = 'move'
                                self.__move_direction = 'left'
                                self.__move_counter = 0
                                self.__anim_counter = 0
                                self.__position = (self.__player.position()[0] * 32 * self.__resolution,
                                                   self.__player.position()[1] * 32 * self.__resolution)
                                for x in range(len(self.__guards)):
                                    self.__guard_positions[x] = (self.__guards[x].position()[0] * 32 * self.__resolution,
                                                       self.__guards[x].position()[1] * 32 * self.__resolution)
                            case pygame.K_s | pygame.K_DOWN:
                                if self.__allow_movement is False:
                                    continue
                                self.__allow_movement = False
                                self.__state = 'move'
                                self.__move_direction = 'down'
                                self.__move_counter = 0
                                self.__anim_counter = 0
                                self.__position = (self.__player.position()[0] * 32 * self.__resolution,
                                                   self.__player.position()[1] * 32 * self.__resolution)
                                for x in range(len(self.__guards)):
                                    self.__guard_positions[x] = (self.__guards[x].position()[0] * 32 * self.__resolution,
                                                       self.__guards[x].position()[1] * 32 * self.__resolution)
                            case pygame.K_d | pygame.K_RIGHT:
                                if self.__allow_movement is False:
                                    continue
                                self.__allow_movement = False
                                self.__state = 'move'
                                self.__move_direction = 'right'
                                self.__move_counter = 0
                                self.__anim_counter = 0
                                self.__position = (self.__player.position()[0] * 32 * self.__resolution,
                                                   self.__player.position()[1] * 32 * self.__resolution)
                                for x in range(len(self.__guards)):
                                    self.__guard_positions[x] = (self.__guards[x].position()[0] * 32 * self.__resolution,
                                                       self.__guards[x].position()[1] * 32 * self.__resolution)
        elif self.__state == 'help':
            for ev in pygame.event.get():
                match ev.type:
                    case pygame.QUIT:
                        self.__running = False
                    case pygame.K_ESCAPE:
                        self.__escape_state()
                    case pygame.KEYDOWN:
                        match ev.key:
                            case pygame.K_m:
                                self.__music.toggle()
                            case pygame.K_ESCAPE | pygame.K_h:
                                self.__state = 'game'
        else:
            for ev in pygame.event.get():
                match ev.type:
                    case pygame.QUIT:
                        self.__running = False
                    case pygame.KEYDOWN:
                        match ev.key:
                            case pygame.K_m:
                                self.__music.toggle()
                            case pygame.K_ESCAPE:
                                self.__escape_state()
                    case pygame.MOUSEBUTTONDOWN:
                        self.__mouse_click(pygame.mouse.get_pos())

    def __move_player(self):
        player_position = self.__player.position()
        if self.__move_counter == 15 // self.__resolution:
            self.__state = 'move_guard'
            match self.__move_direction:
                case 'up':
                    if self.__board.tiles[player_position[1] - 1][player_position[0]].type != "w":
                        self.__player.moveUp()
                case 'down':
                    if self.__board.tiles[player_position[1] + 1][player_position[0]].type != "w":
                        self.__player.moveDown()
                case 'left':
                    if self.__board.tiles[player_position[1]][player_position[0] - 1].type != "w":
                        self.__player.moveLeft()
                case 'right':
                    if self.__board.tiles[player_position[1]][player_position[0] + 1].type != "w":
                        self.__player.moveRight()
        # changes sprites depending on if moving left or right (stays the same with up/down)
        if self.__move_direction == "right" or self.__move_direction == "left":
            self.__player.direction = self.__move_direction
        sprites = self.__player.currSprites()
        step_size = 2 * self.__resolution * self.__resolution
        match self.__move_direction:
            case "right":
                if self.__board.tiles[player_position[1]][player_position[0] + 1].type != "w":
                    # draw background
                    self.__board.draw_level()
                    self.__draw_guards()
                    # draw animation frame
                    self.__screen.foreground_surface.blit(sprites[self.__anim_counter], (self.__position[0],
                                                                                         self.__position[1]))

                    # slight movement + decrement distance left to travel
                    self.__position = (self.__position[0] + step_size, self.__position[1])
                    if not (self.__move_counter % 4):
                        self.__anim_counter += 1

                    # for resetting animation
                    if self.__anim_counter >= len(sprites):
                        self.__anim_counter = 0

                    self.__screen.update()
                    # update player location internally
            case "left":
                if self.__board.tiles[player_position[1]][player_position[0] - 1].type != "w":
                    # draw background
                    self.__board.draw_level()
                    self.__draw_guards()
                    # draw animation frame
                    self.__screen.foreground_surface.blit(sprites[self.__anim_counter],
                                                          (self.__position[0], self.__position[1]))

                    # slight movement + decrement distance left to travel
                    self.__position = (self.__position[0] - step_size, self.__position[1])
                    if not (self.__move_counter % 4):
                        self.__anim_counter += 1

                    # for resetting animation
                    if self.__anim_counter >= len(sprites):
                        self.__anim_counter = 0

                    self.__screen.update()
                    # update player location internally
            case "up":
                if self.__board.tiles[player_position[1] - 1][player_position[0]].type != "w":
                    # draw background
                    self.__board.draw_level()
                    self.__draw_guards()
                    # draw animation frame
                    self.__screen.foreground_surface.blit(sprites[self.__anim_counter],
                                                          (self.__position[0], self.__position[1]))

                    # slight movement + decrement distance left to travel
                    self.__position = (self.__position[0], self.__position[1] - step_size)
                    if not (self.__move_counter % 4):
                        self.__anim_counter += 1

                    # for resetting animation
                    if self.__anim_counter >= len(sprites):
                        self.__anim_counter = 0

                    self.__screen.update()
                    # update player location internally
            case "down":
                if self.__board.tiles[player_position[1] + 1][player_position[0]].type != "w":
                    # draw background
                    self.__board.draw_level()
                    self.__draw_guards()
                    # draw animation frame
                    self.__screen.foreground_surface.blit(sprites[self.__anim_counter],
                                                          (self.__position[0], self.__position[1]))

                    # slight movement + decrement distance left to travel
                    self.__position = (self.__position[0], self.__position[1] + step_size)
                    if not (self.__move_counter % 4):
                        self.__anim_counter += 1

                    # for resetting animation
                    if self.__anim_counter >= len(sprites):
                        self.__anim_counter = 0

                    self.__screen.update()
                    # update player location internally

        player_position = self.__player.position()

        if self.__board.tiles[player_position[1]][player_position[0]].type == "t" and \
                self.__board.tiles[player_position[1]][player_position[0]].lit:
            self.__board.tiles[player_position[1]][player_position[0]].unlight()
            self.__board.torch_check()

    # not done
    def __move_guards(self):
        if self.__move_counter == 15 // self.__resolution:
            self.__state = 'game'
        if self.__anim_counter >= 2:
            self.__anim_counter = 0
        self.__board.draw_level()
        self.__player.draw()
        for x in range(len(self.__guards)):
            sprites = self.__guards[x].currSprites()
            step_size = 2 * self.__resolution * self.__resolution
            move_direction = self.__guard_routes[x][1][(self.__turn_counter % len(self.__guard_routes[x][1]))]
            if self.__guard_tracking:
                move_direction = self.__temp_bfs(self.__guards[x])
            if self.__check_guard_path(self.__guards[x], move_direction) is False:
                self.__guards[x].draw()
                continue
            match move_direction:
                case 'R':
                    # draw background
                    # draw animation frame
                    self.__screen.foreground_surface.blit(self.__guards[x].currSprites()[self.__anim_counter], (self.__guard_positions[x][0],
                                                                      self.__guard_positions[x][1]))
                    # slight movement + decrement distance left to travel
                    self.__guard_positions[x] = (self.__guard_positions[x][0] + step_size, self.__guard_positions[x][1])
                    # update guard location internally
                case 'L':
                    # draw background
                    # draw animation frame
                    self.__screen.foreground_surface.blit(self.__guards[x].currSprites()[self.__anim_counter],
                                                          (self.__guard_positions[x][0],
                                                           self.__guard_positions[x][1]))
                    # slight movement + decrement distance left to travel
                    self.__guard_positions[x] = (self.__guard_positions[x][0] - step_size, self.__guard_positions[x][1])
                case "U":
                    # draw background
                    # draw animation frame
                    self.__screen.foreground_surface.blit(self.__guards[x].currSprites()[self.__anim_counter],
                                                          (self.__guard_positions[x][0],
                                                           self.__guard_positions[x][1]))
                    # slight movement + decrement distance left to travel
                    self.__guard_positions[x] = (self.__guard_positions[x][0], self.__guard_positions[x][1] - step_size)
                case "D":
                    # draw background
                    # draw animation frame
                    self.__screen.foreground_surface.blit(self.__guards[x].currSprites()[self.__anim_counter],
                                                          (self.__guard_positions[x][0],
                                                           self.__guard_positions[x][1]))
                    # slight movement + decrement distance left to travel
                    self.__guard_positions[x] = (self.__guard_positions[x][0], self.__guard_positions[x][1] + step_size)

        if not (self.__move_counter % 5):
            self.__anim_counter += 1

        # for resetting animation
        if self.__anim_counter >= 2:
            self.__anim_counter = 0
        self.__screen.update()

    def __get_spawns(self):
        player_spawn, guards = self.__board.load_level(self.__level)
        return player_spawn, guards

    def __load_game(self):
        self.__music.play_music('game')
        player_spawn, guards = self.__board.load_level(self.__level)
        return player_spawn, guards

    def __check_game_over(self, player_position):
        if self.__board.tiles[player_position[1]][player_position[0]].type == "g":
            return True
        return False

    def __check_next_level(self, player_position):
        if self.__board.tiles[player_position[1]][player_position[0]].type in ['e', 'c']:
            return not self.__board.check_for_key()
        return False

    def __check_key(self, player_position):
        if self.__board.tiles[player_position[1]][player_position[0]].type == "k":
            self.__board.tiles[player_position[1]][player_position[0]] = Tile()
            self.__board.orig_tiles[player_position[1]][player_position[0]] = 'o'
            self.__board.torch_check()
            self.__board.unlock()
            self.__player.key = True
            return True
        return False

    def __draw_guards(self):
        for x in range(len(self.__guards)):
            self.__guards[x].draw()

    def __animate_torches(self):
        if self.__torch_counter % 32 == 0:
            self.__anim_torches = not self.__anim_torches

        width_scale = self.__width // len(self.__board.tiles[0])
        # have to use 15/16 because tiles are scaled for the 15 rows. The 16th is the HUD
        height_scale = 15/16*self.__height // len(self.__board.tiles)
        if self.__anim_torches:
            big_torch = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Torch/Torch_big.png")
            big_torch = pygame.transform.scale(big_torch, (width_scale, height_scale))
            for x in range(len(self.__board.tiles)):
                for y in range(len(self.__board.tiles[0])):
                    # print(self.__board.tiles[x][y].type, end='')
                    if self.__board.tiles[x][y].type == 't' and self.__board.tiles[x][y].lit:
                        # not correct position
                        self.__screen.foreground_surface.blit(big_torch, (self.__board.tiles[x][y].pos[0] * width_scale, self.__board.tiles[x][y].pos[1] * height_scale))

    # Runs the actual game
    def __run_game(self):
        self.__board.draw_level()
        self.__board.display_hud(self.__player.key)
        self.__player.draw()
        self.__draw_guards()
        self.__animate_torches()
        if self.__check_game_over(self.__player.position()):
            self.__music.play_music("game_over")
            self.__level, self.__state = game_over(self.__width, self.__height, self.__screen,
                                                   self.__board, self.__black, (255, 255, 255))
            self.__player_spawn, self.__guard_routes = self.__get_spawns()
            self.__set_player_and_guards()

        self.__check_key(self.__player.position())  # change to if statement if you want to do hud stuff

        if self.__check_next_level(self.__player.position()):
            if self.__level == 3:
                self.__board.unload()
                self.__level, self.__state = win(self.__width, self.__height, self.__screen, self.__black, (255, 255, 255))
                self.__music.play_music("win")
                self.__player_spawn, guards = self.__board.load_level()
                self.__set_player_and_guards()
            else:
                self.__level += 1
                self.__board.unload()
                self.__player_spawn, self.__guard_routes = self.__load_game()
                self.__set_player_and_guards()

    def __check_guard_path(self, guard, direction):
        match direction:
            case 'R':
                if guard.x + 1 > 27:
                    return False
                if self.__board.tiles[guard.y][guard.x + 1].type not in ['o', 't', 'p']:
                    return False
            case 'L':
                if guard.x - 1 < 1:
                    return False
                if self.__board.tiles[guard.y][guard.x - 1].type not in ['o', 't', 'p']:
                    return False
            case 'U':
                if guard.y - 1 < 1:
                    return False
                if self.__board.tiles[guard.y - 1][guard.x].type not in ['o', 't', 'p']:
                    return False
            case 'D':
                if guard.y + 1 > 27:
                    return False
                if self.__board.tiles[guard.y + 1][guard.x].type not in ['o', 't', 'p']:
                    return False
        return True

    def __temp_bfs(self, guard):
        player_x, player_y = self.__player.position()
        visited = [[False for _ in range(27)] for _ in range(27)]
        dx = [0, 0, -1, 1]
        dy = [-1, 1, 0, 0]
        d = ['U', 'D', 'L', 'R']
        q = queue.Queue()
        visited[guard.y][guard.x] = True
        q.put((guard.x, guard.y, 'X'))
        while not q.empty():
            curr_x, curr_y, first_direction = q.get()
            #print(f"{curr_x} {curr_y} {player_x} {player_y} {first_direction}")
            if curr_x == player_x and curr_y == player_y:
                return first_direction
            for i in range(4):
                new_x = curr_x + dx[i]
                new_y = curr_y + dy[i]
                if 0 <= new_x < 27 and 0 <= new_y < 27 and self.__board.tiles[new_y][new_x].type != 'w' and visited[new_y][new_x] is False:
                    visited[new_y][new_x] = True
                    if first_direction == 'X':
                        q.put((new_x, new_y, d[i]))
                    else:
                        q.put((new_x, new_y, first_direction))
        return d[0]

    def __update_guards(self):
        for x in range(len(self.__guards)):
            move_direction = self.__guard_routes[x][1][(self.__turn_counter % len(self.__guard_routes[x][1]))]
            if self.__guard_tracking:
                move_direction = self.__temp_bfs(self.__guards[x])
            match move_direction:
                case 'R':
                    if self.__check_guard_path(self.__guards[x], 'R'):
                        self.__guards[x].moveRight()
                case 'L':
                    if self.__check_guard_path(self.__guards[x], 'L'):
                        self.__guards[x].moveLeft()
                case 'U':
                    if self.__check_guard_path(self.__guards[x], 'U'):
                        self.__guards[x].moveUp()
                case 'D':
                    if self.__check_guard_path(self.__guards[x], 'D'):
                        self.__guards[x].moveDown()
            self.__board.replace_tile_with_guard(self.__guards[x].y, self.__guards[x].x, self.__guards[x].currSprites()[0])
            self.__board.torch_check()
        self.__turn_counter = self.__turn_counter + 1

    # Main execution loop
    def run(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        clock = pygame.time.Clock()
        self.__move_counter = 0
        self.__torch_counter = 0
        self.__move_flag = False
        while self.__running:
            clock.tick(60)

            self.__move_counter += 1
            if self.__move_counter >= 16 // self.__resolution:
                self.__move_counter = 0

            self.__torch_counter += 1
            if self.__torch_counter >= 64:
                self.__torch_counter = 0

            self.__handle_events()
            match self.__state:
                case 'menu':
                    pygame.mouse.set_visible(True)
                    self.__music.play_music('menu')
                    run_menu(self.__width, self.__height, self.__rects, self.__screen,
                             self.__torch_counter, self.__anim_torches, self.__white)
                case 'options':
                    pygame.mouse.set_visible(True)
                    run_options(self.__width, self.__height, self.__rects, self.__screen, self.__torch_counter,
                                self.__anim_torches, (255, 255, 255), self.__white, self.__difficulty)
                case 'game':
                    pygame.mouse.set_visible(False)
                    if self.__move_flag == "guard":
                        self.__update_guards()
                        if self.__guard_turn_counter < self.__guard_difficulty and not self.__check_game_over(self.__player.position()):
                            self.__state = 'move_guard'
                            self.__move_flag = "player"
                            continue
                    self.__allow_movement = True
                    self.__guard_turn_counter = 0
                    self.__move_flag = "none"
                    try:
                        self.__run_game()
                    except Exception as E:
                        print("Attempted to load a game asset but failed (this try/except is in run(self) method):", E)
                case 'help':
                    display_help(self.__width, self.__height, self.__resolution, self.__screen)
                case 'game_over':
                    pass
                case 'move':
                    if self.__move_flag == "none":
                        self.__move_flag = "player"
                    self.__move_player()
                case 'move_guard':
                    if self.__move_flag == "player":
                        if self.__check_game_over(self.__player.position()):
                            self.__music.play_music("game_over")
                            self.__level, self.__state = game_over(self.__width, self.__height, self.__screen,
                                                                   self.__board, self.__black, (255, 255, 255))

                            self.__player_spawn, self.__guard_routes = self.__get_spawns()
                            self.__set_player_and_guards()
                            continue
                        self.__guard_turn_counter = self.__guard_turn_counter + 1
                        self.__move_counter = 0
                        self.__anim_counter = 0
                        self.__move_flag = "guard"
                        for x in range(len(self.__guards)):
                            move_direction = self.__guard_routes[x][1][(self.__turn_counter % len(self.__guard_routes[x][1]))]
                            if self.__guard_tracking:
                                move_direction = self.__temp_bfs(self.__guards[x])
                            match move_direction:
                                case 'R':
                                    self.__guards[x].direction = 'right'
                                case 'L':
                                    self.__guards[x].direction = 'left'
                            self.__board.replace_tile_with_original(self.__guards[x].y, self.__guards[x].x)
                    self.__move_guards()
            self.__screen.update()
        pygame.quit()
