import queue
from pathlib import Path
import pygame
import os
import igraph as ig
import time
from intheshadows.print import display_help, run_menu, run_options, display_inventory, loading_screen
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
        (self.__width, self.__height) = (64 * 28, 64 * 16)

        self.__level = self.load_level()
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

        self.__vertices = []

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

        self.__water_flask = pygame.transform.scale(
            pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/water_flask.png").convert_alpha(),
            (self.__resolution * 32, self.__resolution * 32))

    def save_level(self):
        save_file = Path(__file__).parent / "user_progress.txt"
        with open(save_file, 'w') as file:
            file.write(str(self.__level))

    def load_level(self):
        # edit this and user_progress.txt to save future info like torches lit and moves etc
        save_file = Path(__file__).parent / "user_progress.txt"
        save_file.touch(exist_ok=True)  # checks if exists if not creates file
        if save_file.stat().st_size != 0:
            # if file is has saved progress
            with open(save_file, 'r') as file:
                return int(file.read())
        else:
            return 1

    def __set_player_and_guards(self):
        self.__player = Player(self.__screen.foreground_surface, self.__player_spawn[0], self.__player_spawn[1],
                               self.__resolution)
        self.__guards = []
        self.__guard_positions.clear()
        self.__guard_returning = []
        self.__turn_counter = []
        self.__guard_tracking = False
        for x in range(len(self.__guard_routes)):
            self.__guards.append(
                Guard(self.__screen.foreground_surface, self.__resolution, self.__guard_routes[x][0][0],
                      self.__guard_routes[x][0][1], self.__guard_routes[x][1],
                      self.__difficulty))
            self.__guard_positions.append(())
            self.__guard_returning.append(False)
            self.__turn_counter.append(0)

    # Changes states when escape is pressed
    def __escape_state(self):
        match self.__state:
            case 'load':
                self.__state = 'game'
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
            case 'inventory':
                self.__state = 'game'

    # Changes state based on button click
    def __mouse_click(self, mouse_pos):
        if self.__state == 'menu':
            if self.__rects['start_text_rect'].collidepoint(mouse_pos):
                self.__state = 'load'
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
            keys = pygame.key.get_pressed()
            if True in keys:
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, unicode="w", key=pygame.K_w, mod=pygame.KMOD_NONE))
                elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, unicode="a", key=pygame.K_a, mod=pygame.KMOD_NONE))
                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    pygame.event.post(
                        pygame.event.Event(pygame.KEYDOWN, unicode="s", key=pygame.K_s, mod=pygame.KMOD_NONE))
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    pygame.event.post(
                        pygame.event.Event(pygame.KEYDOWN, unicode="d", key=pygame.K_d, mod=pygame.KMOD_NONE))

            for ev in pygame.event.get():
                match ev.type:
                    case pygame.QUIT:
                        self.__running = False
                    case pygame.KEYDOWN:
                        match ev.key:
                            case pygame.K_SPACE:
                                if self.__player.dash_cooldown == 0:
                                    self.__player.dash = True
                                    self.__player.dash_cooldown = 4
                                else:
                                    self.__player.dash = False
                            case pygame.K_1:
                                self.__player.extinguish = True
                            case pygame.K_2:
                                self.__player.smoke = True
                            case pygame.K_h:  # help screen in game
                                self.__state = 'help'
                            case pygame.K_i:
                                self.__state = 'inventory'
                            case pygame.K_m:
                                self.__music.toggle()
                            case pygame.K_k:
                                if self.__guard_tracking:
                                    self.__alert_mode_off()
                                else:
                                    self.__alert_mode_on()
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
                                    self.__guard_positions[x] = (
                                        self.__guards[x].position()[0] * 32 * self.__resolution,
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
                                    self.__guard_positions[x] = (
                                        self.__guards[x].position()[0] * 32 * self.__resolution,
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
                                    self.__guard_positions[x] = (
                                        self.__guards[x].position()[0] * 32 * self.__resolution,
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
                                    self.__guard_positions[x] = (
                                        self.__guards[x].position()[0] * 32 * self.__resolution,
                                        self.__guards[x].position()[1] * 32 * self.__resolution)
        elif self.__state == 'load':
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_r:
                        self.__level = 1
                        self.save_level()
                if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                    self.__state = 'game'
                    self.__board.unload()
                    self.__player_spawn, self.__guard_routes = self.__load_game()
                    self.__set_player_and_guards()
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
        elif self.__state == 'inventory':
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
                            case pygame.K_ESCAPE:
                                self.__escape_state()
                            case pygame.K_ESCAPE | pygame.K_i:
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

    def __guard_near_player(self):
        player_box = [(self.__player.position()[0] - 1, self.__player.position()[1] - 1), (self.__player.position()[0], self.__player.position()[1] - 1), (self.__player.position()[0] + 1, self.__player.position()[1] - 1),
                      (self.__player.position()[0] - 1, self.__player.position()[1]), (self.__player.position()[0], self.__player.position()[1]), (self.__player.position()[0] + 1, self.__player.position()[1]),
                      (self.__player.position()[0] - 1, self.__player.position()[1] + 1), (self.__player.position()[0], self.__player.position()[1] + 1), (self.__player.position()[0] + 1, self.__player.position()[1] + 1)]
        for guard in self.__guards:
            if guard.position() in player_box:
                return True
        return False

    def __move_player(self):
        dashed = False  # if player dashed, torch will be lit, conditional at end of function
        extinguished = False
        player_position = self.__player.position()
        if self.__move_counter == 31 // self.__resolution:
            self.__state = 'move_guard'
            match self.__move_direction:
                case 'up':
                    if self.__player.extinguish:
                        extinguished = True
                        tempY = player_position[1] - 1
                        while tempY > 0:
                            self.__screen.foreground_surface.blit(self.__water_flask, (player_position[0] * 32 * self.__resolution, tempY * 32 * self.__resolution))
                            self.__screen.update()
                            time.sleep(0.01)
                            if self.__board.tiles[tempY][player_position[0]].type == "w":
                                break
                            if self.__board.tiles[tempY][player_position[0]].type == "t":
                                self.__board.tiles[tempY][player_position[0]].unlight()
                                break
                            if self.__board.tiles[tempY][player_position[0]].type == "g":
                                self.__alert_mode_on()
                                break
                            tempY -= 1
                        self.__player.extinguish = False
                    elif self.__board.tiles[player_position[1] - 1][player_position[0]].type != "w":
                        if self.__player.dash and self.__board.tiles[player_position[1] - 2][player_position[0]].type != "w":
                            self.__player.moveUp()
                            self.__check_key(self.__player.position())
                            self.__player.moveUp()
                            dashed = True
                            self.__player.dash_counter = 4
                        else:
                            self.__player.moveUp()
                    if self.__player.dash_cooldown > 0 and not dashed:
                        self.__player.dash_cooldown -= 1
                    self.__player.dash = False  # reset dash conditional so next turn isnt if user was by a wall etc
                case 'down':
                    if self.__player.extinguish:
                        extinguished = True
                        tempY = player_position[1] + 1
                        while tempY < 15:
                            self.__screen.foreground_surface.blit(self.__water_flask, (player_position[0] * 32 * self.__resolution, tempY * 32 * self.__resolution))
                            self.__screen.update()
                            time.sleep(0.01)
                            if self.__board.tiles[tempY][player_position[0]].type == "w":
                                break
                            if self.__board.tiles[tempY][player_position[0]].type == "t":
                                self.__board.tiles[tempY][player_position[0]].unlight()
                                break
                            if self.__board.tiles[tempY][player_position[0]].type == "g":
                                self.__alert_mode_on()
                                break
                            tempY += 1
                        self.__player.extinguish = False
                    elif self.__board.tiles[player_position[1] + 1][player_position[0]].type != "w":
                        if self.__player.dash and self.__board.tiles[player_position[1] + 2][player_position[0]].type != "w":
                            self.__player.moveDown()
                            self.__check_key(self.__player.position())
                            self.__player.moveDown()
                            dashed = True
                            self.__player.dash_counter = 4
                        else:
                            self.__player.moveDown()
                    if self.__player.dash_cooldown > 0:
                        self.__player.dash_cooldown -= 1
                    self.__player.dash = False  # reset dash conditional so next turn isnt if user was by a wall etc
                case 'left':
                    if self.__player.extinguish:
                        extinguished = True
                        tempX = player_position[0] - 1
                        while tempX > 0:
                            self.__screen.foreground_surface.blit(self.__water_flask, (tempX * 32 * self.__resolution, player_position[1] * 32 * self.__resolution))
                            self.__screen.update()
                            time.sleep(0.01)
                            if self.__board.tiles[player_position[1]][tempX].type == "w":
                                break
                            if self.__board.tiles[player_position[1]][tempX].type == "t":
                                self.__board.tiles[player_position[1]][tempX].unlight()
                                break
                            if self.__board.tiles[player_position[1]][tempX].type == "g":
                                self.__alert_mode_on()
                                break
                            tempX -= 1
                        self.__player.extinguish = False
                    elif self.__board.tiles[player_position[1]][player_position[0] - 1].type != "w":
                        if self.__player.dash and self.__board.tiles[player_position[1]][player_position[0] - 2].type != "w":
                            self.__player.moveLeft()
                            self.__check_key(self.__player.position())
                            self.__player.moveLeft()
                            dashed = True
                            self.__player.dash_counter = 4
                        else:
                            self.__player.moveLeft()
                    if self.__player.dash_cooldown > 0:
                        self.__player.dash_cooldown -= 1
                    self.__player.dash = False  # reset dash conditional so next turn isnt if user was by a wall etc
                case 'right':
                    if self.__player.extinguish:
                        extinguished = True
                        tempX = player_position[0] + 1
                        while tempX < 28:
                            self.__screen.foreground_surface.blit(self.__water_flask, (tempX * 32 * self.__resolution, player_position[1] * 32 * self.__resolution))
                            self.__screen.update()
                            time.sleep(0.01)
                            if self.__board.tiles[player_position[1]][tempX].type == "w":
                                break
                            if self.__board.tiles[player_position[1]][tempX].type == "t":
                                self.__board.tiles[player_position[1]][tempX].unlight()
                                break
                            if self.__board.tiles[player_position[1]][tempX].type == "g":
                                self.__alert_mode_on()
                                break
                            tempX += 1
                        self.__player.extinguish = False
                    elif self.__board.tiles[player_position[1]][player_position[0] + 1].type != "w":
                        if self.__player.dash and self.__board.tiles[player_position[1]][player_position[0] + 2].type != "w":
                            self.__player.moveRight()
                            self.__check_key(self.__player.position())
                            self.__player.moveRight()
                            dashed = True
                            self.__player.dash_counter = 4
                        else:
                            self.__player.moveRight()
                    if self.__player.dash_cooldown > 0:
                        self.__player.dash_cooldown -= 1
                    self.__player.dash = False  # reset dash conditional so next turn isnt if user was by a wall etc
        # changes sprites depending on if moving left, right, up, or down
        self.__player.direction = self.__move_direction
        self.__player.update_sprites()
        sprites = self.__player.currSprites()
        if self.__player.extinguish:
            return
        step_size = 1 * self.__resolution * self.__resolution
        if self.__player.dash:
            step_size = 2 * self.__resolution * self.__resolution
        anim_spd = 4 // self.__resolution
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
                    if not (self.__move_counter % anim_spd):
                        self.__anim_counter += 1

                    # for resetting animation
                    if self.__anim_counter >= len(sprites):
                        self.__anim_counter = 0

                    self.__screen.update()
                    # update player location internally
                if dashed:
                    if self.__board.tiles[player_position[1]][player_position[0] + 1].type == "t" and \
                            self.__board.tiles[player_position[1]][player_position[0] + 1].lit:
                        self.__board.tiles[player_position[1]][player_position[0] + 1].unlight()
                        self.__board.torch_check()

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
                    if not (self.__move_counter % anim_spd):
                        self.__anim_counter += 1

                    # for resetting animation
                    if self.__anim_counter >= len(sprites):
                        self.__anim_counter = 0

                    self.__screen.update()
                    # update player location internally
                if dashed:
                    if self.__board.tiles[player_position[1]][player_position[0] - 1].type == "t" and \
                            self.__board.tiles[player_position[1]][player_position[0] - 1].lit:
                        self.__board.tiles[player_position[1]][player_position[0] - 1].unlight()
                        self.__board.torch_check()

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
                    if not (self.__move_counter % anim_spd):
                        self.__anim_counter += 1

                    # for resetting animation
                    if self.__anim_counter >= len(sprites):
                        self.__anim_counter = 0

                    self.__screen.update()
                    # update player location internally

                if dashed:
                    if self.__board.tiles[player_position[1] - 1][player_position[0]].type == "t" and \
                            self.__board.tiles[player_position[1] - 1][player_position[0]].lit:
                        self.__board.tiles[player_position[1] - 1][player_position[0]].unlight()
                        self.__board.torch_check()

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
                    if not (self.__move_counter % anim_spd):
                        self.__anim_counter += 1

                    # for resetting animation
                    if self.__anim_counter >= len(sprites):
                        self.__anim_counter = 0

                    self.__screen.update()
                    # update player location internally
                if dashed:
                    if self.__board.tiles[player_position[1] + 1][player_position[0]].type == "t" and \
                            self.__board.tiles[player_position[1] + 1][player_position[0]].lit:
                        self.__board.tiles[player_position[1] + 1][player_position[0]].unlight()
                        self.__board.torch_check()
        if self.__player.smoke and self.__guard_near_player():
            self.__alert_mode_off()
            self.__player.smoke = False
        player_position = self.__player.position()
        if self.__board.tiles[player_position[1]][player_position[0]].type == "t" and \
                self.__board.tiles[player_position[1]][player_position[0]].lit:
            self.__board.tiles[player_position[1]][player_position[0]].unlight()
            self.__board.torch_check()

    # not done
    def __move_guards(self):
        if self.__move_counter == 31 // self.__resolution:
            self.__state = 'game'
        self.__board.draw_level()
        self.__player.draw()
        for x in range(len(self.__guards)):
            step_size = 1 * self.__resolution * self.__resolution
            move_direction = self.__guard_routes[x][1][(self.__turn_counter[x] % len(self.__guard_routes[x][1]))]
            if self.__guard_tracking:
                move_direction = self.__shortest_path((self.__guards[x].x, self.__guards[x].y),
                                                      self.__player.position())
            elif self.__guard_returning[x]:
                move_direction = self.__shortest_path((self.__guards[x].x, self.__guards[x].y),
                                                      self.__guard_position_before_tracking[x])
            if self.__check_guard_path(self.__guards[x], move_direction) is False:
                self.__guards[x].draw()
                continue
            self.__guards[x].update_sprites()
            match move_direction:
                case 'R':
                    # draw background
                    # draw animation frame
                    self.__screen.foreground_surface.blit(self.__guards[x].currSprites()[self.__anim_counter],
                                                          (self.__guard_positions[x][0],
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
        if self.__anim_counter >= 4:
            self.__anim_counter = 0
        self.__screen.update()

    def __get_spawns(self):
        player_spawn, guards = self.__board.load_level(self.__level)
        return player_spawn, guards

    def __load_game(self):
        self.__music.play_music('game')
        player_spawn, guards = self.__board.load_level(self.__level)
        self.__vertices = ig.Graph()
        count = 0
        for i in self.__board.tiles:
            for j in i:
                count += 1
        self.__vertices.add_vertices(count)
        width = len(self.__board.tiles[0])
        height = len(self.__board.tiles)
        for i, mains in enumerate(self.__board.tiles):
            for j, nexts in enumerate(mains):
                if nexts.type != 'w':
                    if j != 0:
                        if self.__board.tiles[i][j - 1].type != 'w':
                            self.__vertices.add_edge(j + (i * width), (j - 1) + (i * width))
                    if j != (width - 1):
                        if self.__board.tiles[i][j + 1].type != 'w':
                            self.__vertices.add_edge(j + (i * width), (j + 1) + (i * width))
                    if i != 0:
                        if self.__board.tiles[i - 1][j].type != 'w':
                            self.__vertices.add_edge(j + (i * width), j + ((i - 1) * width))
                    if i != (height - 1):
                        if self.__board.tiles[i + 1][j].type != 'w':
                            self.__vertices.add_edge(j + (i * width), j + ((i + 1) * width))
        self.__vertices = self.__vertices.simplify()
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

        width_scale = self.__width // len(self.__board.tiles[0])
        # have to use 15/16 because tiles are scaled for the 15 rows. The 16th is the HUD
        height_scale = 15 / 16 * self.__height // len(self.__board.tiles)
        if self.__anim_torches:
            big_torch = pygame.image.load(Path(__file__).parent / "assets/graphics/Level Elements/Torch/Torch_big.png")
            big_torch = pygame.transform.scale(big_torch, (width_scale, height_scale))
            for x in range(len(self.__board.tiles)):
                for y in range(len(self.__board.tiles[0])):
                    # print(self.__board.tiles[x][y].type, end='')
                    if self.__board.tiles[x][y].type == 't' and self.__board.tiles[x][y].lit:
                        # not correct position
                        self.__screen.foreground_surface.blit(big_torch, (
                            self.__board.tiles[x][y].pos[0] * width_scale,
                            self.__board.tiles[x][y].pos[1] * height_scale))

    # Runs the actual game
    def __run_game(self):
        self.__board.draw_level()
        self.__board.display_hud(self.__player.key)
        self.__player.draw()
        self.__draw_guards()
        if self.__check_game_over(self.__player.position()):
            self.__music.play_music("game_over")
            self.__level, self.__state = game_over(self.__width, self.__height, self.__screen,
                                                   self.__board)
            self.__player_spawn, self.__guard_routes = self.__get_spawns()
            self.__set_player_and_guards()
            self.__guard_tracking = False

        self.__check_key(self.__player.position())  # change to if statement if you want to do hud stuff

        if self.__check_next_level(self.__player.position()):
            if self.__level == 3:
                self.__board.unload()
                self.__level, self.__state = win(self.__width, self.__height, self.__screen, self.__black,
                                                 (255, 255, 255))
                self.__music.play_music("win")
                self.__player_spawn, guards = self.__board.load_level()
                self.__set_player_and_guards()
                if self.__guard_tracking:
                    self.__alert_mode_on()
            else:
                self.__level += 1
                self.__board.unload()
                self.__player_spawn, self.__guard_routes = self.__load_game()
                self.__set_player_and_guards()
                if self.__guard_tracking:
                    self.__alert_mode_off()

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

    def __shortest_path(self, start, end):
        width = len(self.__board.tiles[0])
        height = len(self.__board.tiles)
        start_num = (start[1] * width) + start[0]
        end_num = (end[1] * width) + end[0]
        shortest = self.__vertices.get_shortest_paths(start_num, end_num)
        dist = shortest[0][1] - shortest[0][0]
        if dist == 1:
            return 'R'
        elif dist == -1:
            return 'L'
        elif dist == width:
            return 'D'
        elif dist == -1 * width:
            return 'U'
        return 'H'

    def __alert_mode_on(self):
        self.__guard_tracking = True
        self.__music.play_music('alert')
        self.__guard_position_before_tracking = []
        for i in range(0, len(self.__guards)):
            self.__guard_position_before_tracking.append((self.__guards[i].x, self.__guards[i].y))

    def __alert_mode_off(self):
        self.__guard_tracking = False
        self.__music.play_music('game')
        self.__guard_returning = []
        for i in range(0, len(self.__guards)):
            self.__guard_returning.append(True)

    def __check_guard_vision(self):
        player_position = self.__player.position()
        for x in range(len(self.__guards)):
            guard_x = self.__guards[x].x
            guard_y = self.__guards[x].y
            match self.__guards[x].direction:
                case "up":
                    dx = [-1, 0, 1, -1, 0, 1]
                    dy = [-1, -1, -1, -2, -2, -2]
                case "down":
                    dx = [-1, 0, 1, -1, 0, 1]
                    dy = [1, 1, 1, 2, 2, 2]
                case "right":
                    dx = [1, 1, 1, 2, 2, 2]
                    dy = [-1, 0, 1, -1, 0, 1]
                case "left":
                    dx = [-1, -1, -1, -2, -2, -2]
                    dy = [-1, 0, 1, -1, 0, 1]
            for i in range(0, 6):
                try:
                    if guard_y + dy[i] == player_position[1] and guard_x + dx[i] == player_position[0]:
                        self.__alert_mode_on()
                        break
                except:
                    pass

    def __update_guards(self):
        for x in range(len(self.__guards)):
            move_direction = self.__guard_routes[x][1][(self.__turn_counter[x] % len(self.__guard_routes[x][1]))]
            if self.__guard_tracking:
                move_direction = self.__shortest_path((self.__guards[x].x, self.__guards[x].y),
                                                      self.__player.position())
                self.__turn_counter[x] = self.__turn_counter[x] - 1
            elif self.__guard_returning[x]:
                self.__turn_counter[x] = self.__turn_counter[x] - 1
                move_direction = self.__shortest_path((self.__guards[x].x, self.__guards[x].y),
                                                      self.__guard_position_before_tracking[x])
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
            self.__board.replace_tile_with_guard(self.__guards[x].y, self.__guards[x].x,
                                                 self.__guards[x].currSprites()[0])
            self.__board.torch_check()
            self.__turn_counter[x] = self.__turn_counter[x] + 1
            if self.__guard_returning[x]:
                if (self.__guards[x].x, self.__guards[x].y) == self.__guard_position_before_tracking[x]:
                    self.__guard_returning[x] = False

    # Main execution loop
    def run(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        clock = pygame.time.Clock()
        self.__move_counter = 0
        self.__torch_counter = 0
        self.__move_flag = False
        while self.__running:
            clock.tick(60)
            # print(clock.get_fps())

            self.__move_counter += 1
            if self.__move_counter >= 32 // self.__resolution:
                self.__move_counter = 0

            self.__torch_counter += 1
            if self.__torch_counter >= 16:
                self.__torch_counter = 0
                self.__anim_torches = not self.__anim_torches

            self.__handle_events()
            match self.__state:
                case 'load':
                    pygame.mouse.set_visible(False)
                    loading_screen(self.__width, self.__height, self.__resolution, self.__screen, self.__level)
                case 'menu':
                    pygame.mouse.set_visible(True)
                    self.__music.play_music('menu')
                    run_menu(self.__width, self.__height, self.__rects, self.__screen,
                             self.__anim_torches)
                case 'options':
                    pygame.mouse.set_visible(True)
                    run_options(self.__width, self.__height, self.__rects, self.__screen,
                                self.__anim_torches, self.__difficulty)
                case 'game':
                    pygame.mouse.set_visible(False)
                    if self.__move_flag == "guard":
                        self.__update_guards()
                        if self.__guard_turn_counter < self.__guard_difficulty and not self.__check_game_over(
                                self.__player.position()):
                            self.__state = 'move_guard'
                            self.__move_flag = "player"
                            continue
                        if self.__guard_tracking is False:
                            self.__check_guard_vision()
                    self.__allow_movement = True
                    self.__guard_turn_counter = 0
                    self.__move_flag = "none"
                    try:
                        self.__run_game()
                    except Exception as E:
                        print("Attempted to load a game asset but failed (this try/except is in run(self) method):", E)
                case 'help':
                    display_help(self.__width, self.__height, self.__resolution, self.__screen)
                case 'inventory':
                    display_inventory(self.__width, self.__height, self.__resolution, self.__screen, self.__player)
                    '''
                    TODO: Add some sort of data structure to store player inventory and pass it to display_inventory
                    also have it track what items are used etc
                    '''
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
                                                                   self.__board)

                            self.__player_spawn, self.__guard_routes = self.__get_spawns()
                            self.__set_player_and_guards()
                            continue
                        if self.__guard_tracking is False:
                            self.__check_guard_vision()
                        self.__guard_turn_counter = self.__guard_turn_counter + 1
                        self.__move_counter = 0
                        self.__anim_counter = 0
                        self.__move_flag = "guard"
                        for x in range(len(self.__guards)):
                            move_direction = self.__guard_routes[x][1][
                                (self.__turn_counter[x] % len(self.__guard_routes[x][1]))]
                            if self.__guard_tracking:
                                self.__shortest_path((self.__guards[x].x, self.__guards[x].y), self.__player.position())
                            elif self.__guard_returning[x]:
                                move_direction = self.__shortest_path((self.__guards[x].x, self.__guards[x].y),
                                                                      self.__guard_position_before_tracking[x])
                            match move_direction:
                                case 'R':
                                    self.__guards[x].direction = 'right'
                                case 'L':
                                    self.__guards[x].direction = 'left'
                                case 'U':
                                    self.__guards[x].direction = 'up'
                                case 'D':
                                    self.__guards[x].direction = 'down'
                            self.__board.replace_tile_with_original(self.__guards[x].y, self.__guards[x].x)
                    self.__move_guards()
            self.__screen.update()
        self.save_level()
        pygame.quit()
