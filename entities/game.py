import pygame
import os
from entities.guard import Guard
from entities.tile import Tile
from entities.window import Window
from entities.music import Music
from entities.board import Board
from entities.player import Player


class Game:
    def __init__(self):
        # Create global variables for height, width, and black and white colors
        self.__black = (0, 0, 0)
        self.__white = (255, 255, 255)
        (self.__width, self.__height) = (64*28, 64*16)

        self.__level = 1
        self.__move_counter = 0
        self.__move_direction = 'right'
        self.__anim_counter = 0

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

        self.__position = ()

        self.__player_spawn, self.__guard_routes = self.__get_spawns()

        self.__set_player_and_guards()

        self.__fullscreen = True

    def __set_player_and_guards(self):
        self.__player = Player(self.__screen.foreground_surface, self.__player_spawn[0], self.__player_spawn[1],
                               self.__resolution)
        self.__guards = []
        for x in range(len(self.__guard_routes)):
            self.__guards.append(Guard(self.__screen.foreground_surface, self.__resolution, self.__guard_routes[x][1][0],
                                       self.__guard_routes[x][1][1], self.__guard_routes[x][2],
                                       self.__guard_routes[x][0]))
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

    # Changes state based on button click
    def __mouse_click(self, mouse_pos):
        if self.__state == 'menu':
            if self.__rects['start_text_rect'].collidepoint(mouse_pos):
                self.__state = 'game'
                self.__board.unload()
                self.__player_spawn, self.__guard_routes = self.__load_game()
            elif self.__rects['options_text_rect'].collidepoint(mouse_pos):
                self.__state = 'options'
            elif self.__rects['quit_text_rect'].collidepoint(mouse_pos):
                self.__running = False
        elif self.__state == 'options':
            if self.__rects['easy_difficulty_rect'].collidepoint(mouse_pos):
                self.__difficulty = "EASY"
            elif self.__rects['medium_difficulty_rect'].collidepoint(mouse_pos):
                self.__difficulty = "MEDIUM"
            elif self.__rects['hard_difficulty_rect'].collidepoint(mouse_pos):
                self.__difficulty = "HARD"
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
                    pygame.display.toggle_fullscreen()
                    self.__fullscreen = True

    # Handles quitting, key presses, and mouse clicks, including in game
    def __handle_events(self):
        if self.__state == 'game':
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
                            case pygame.K_w | pygame.K_UP:
                                self.__state = 'move'
                                self.__move_direction = 'up'
                                self.__move_counter = 0
                                self.__anim_counter = 0
                                self.__turn_counter = self.__turn_counter + 1
                                self.__position = (self.__player.position()[0] * 32 * self.__resolution,
                                                   self.__player.position()[1] * 32 * self.__resolution)
                            case pygame.K_a | pygame.K_LEFT:
                                self.__state = 'move'
                                self.__move_direction = 'left'
                                self.__move_counter = 0
                                self.__anim_counter = 0
                                self.__turn_counter = self.__turn_counter + 1
                                self.__position = (self.__player.position()[0] * 32 * self.__resolution,
                                                   self.__player.position()[1] * 32 * self.__resolution)
                            case pygame.K_s | pygame.K_DOWN:
                                self.__state = 'move'
                                self.__move_direction = 'down'
                                self.__move_counter = 0
                                self.__anim_counter = 0
                                self.__turn_counter = self.__turn_counter + 1
                                self.__position = (self.__player.position()[0] * 32 * self.__resolution,
                                                   self.__player.position()[1] * 32 * self.__resolution)
                            case pygame.K_d | pygame.K_RIGHT:
                                self.__state = 'move'
                                self.__move_direction = 'right'
                                self.__move_counter = 0
                                self.__anim_counter = 0
                                self.__turn_counter = self.__turn_counter + 1
                                self.__position = (self.__player.position()[0] * 32 * self.__resolution,
                                                   self.__player.position()[1] * 32 * self.__resolution)
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

    # Runs the main menu
    def __run_menu(self):
        self.__music.play_music('menu')
        self.__screen.background_surface.fill((0, 0, 0))
        self.__screen.foreground_surface.fill((0, 0, 0, 0))
        big_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(self.__height * 0.2))
        small_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(self.__height * 0.15))

        (start_width, start_height) = (self.__width // 2, self.__height // 2)
        (options_width, options_height) = (start_width, start_height + start_height // 32)
        (quit_width, quit_height) = (start_width, start_height + start_height // 4)

        # text = big_font.render('IN  THE  SHADOWS', True, self.__white)
        # text_rect = text.get_rect()
        # text_rect.center = (self.__width // 2, self.__height // 4)

        start_text = small_font.render('START__', True, self.__white)
        self.__rects['start_text_rect'] = start_text.get_rect()
        self.__rects['start_text_rect'].center = (1.04*start_width, 0.95*start_height)

        options_text = small_font.render('OPTIONS_', True, self.__white)
        self.__rects['options_text_rect'] = options_text.get_rect()
        self.__rects['options_text_rect'].center = (1.02*options_width, options_height + 1.25*options_height // 4)

        quit_text = small_font.render('QUIT__', True, self.__white)
        self.__rects['quit_text_rect'] = quit_text.get_rect()
        self.__rects['quit_text_rect'].center = (1.02*quit_width, quit_height + 1.6*quit_height // 4)

        background = pygame.image.load("assets/graphics/Backgrounds/Home_screen_1.png")
        background = pygame.transform.scale(background, (self.__width, self.__height))

        self.__screen.background_surface.blit(background, (0, 0))
        # self.__screen.background_surface.blit(text, text_rect)
        # self.__screen.background_surface.blit(start_text, self.__rects['start_text_rect'])
        # self.__screen.background_surface.blit(options_text, self.__rects['options_text_rect'])
        # self.__screen.background_surface.blit(quit_text, self.__rects['quit_text_rect'])

    # Runs the options
    def __run_options(self):
        background = pygame.image.load("assets/graphics/Backgrounds/woodBackground.png")
        background = pygame.transform.scale(background, (self.__width, self.__height))
        self.__screen.background_surface.fill(self.__black)
        self.__screen.background_surface.blit(background, (0, 0))

        big_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(self.__height * 0.2))
        small_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(self.__height * 0.09))

        (opt_width, opt_height) = (self.__width // 2, self.__height // 8)
        text = big_font.render('OPTIONS', True, self.__white)
        text_rect = text.get_rect()
        text_rect.center = (opt_width, opt_height)
        self.__screen.background_surface.blit(text, text_rect)

        (diff_width, diff_height) = (opt_width // 2, opt_height + self.__height // 6)
        difficulty = small_font.render('SELECT DIFFICULTY', True, (255, 255, 255))
        difficulty_rect = difficulty.get_rect()
        difficulty_rect.center = (diff_width, diff_height)
        self.__screen.background_surface.blit(difficulty, difficulty_rect)

        (easy_width, easy_height) = (diff_width, diff_height + self.__height // 8)
        easy_difficulty = small_font.render('EASY', True, (0, 153, 0))
        self.__rects['easy_difficulty_rect'] = easy_difficulty.get_rect()
        self.__rects['easy_difficulty_rect'].center = (easy_width, easy_height)
        self.__screen.background_surface.blit(easy_difficulty, self.__rects['easy_difficulty_rect'])

        (med_width, med_height) = (diff_width, easy_height + self.__height // 8)
        medium_difficulty = small_font.render('MEDIUM', True, (255, 128, 0))
        self.__rects['medium_difficulty_rect'] = medium_difficulty.get_rect()
        self.__rects['medium_difficulty_rect'].center = (med_width, med_height)
        self.__screen.background_surface.blit(medium_difficulty, self.__rects['medium_difficulty_rect'])

        (hard_width, hard_height) = (diff_width, med_height + self.__height // 8)
        hard_difficulty = small_font.render('HARD', True, (255, 0, 0))
        self.__rects['hard_difficulty_rect'] = hard_difficulty.get_rect()
        self.__rects['hard_difficulty_rect'].center = (hard_width, hard_height)
        self.__screen.background_surface.blit(hard_difficulty, self.__rects['hard_difficulty_rect'])

        match self.__difficulty:
            case "EASY":
                color = (0, 153, 0)
            case "MEDIUM":
                color = (255, 128, 0)
            case "HARD":
                color = (255, 0, 0)
            case _:
                color = (255, 255, 255)
        text = small_font.render(str(self.__difficulty) + "  MODE  CHOSEN!", True, color)
        text_rect = text.get_rect()
        text_rect.center = (diff_width, hard_height + self.__height // 8)
        self.__screen.background_surface.blit(text, text_rect)

        (res_width, res_height) = (self.__width - self.__width // 4, opt_height + self.__height // 6)
        resolution = small_font.render('SELECT  RESOLUTION', True, self.__white)
        resolution_rect = resolution.get_rect()
        resolution_rect.center = (res_width, res_height)
        self.__screen.background_surface.blit(resolution, resolution_rect)

        (res_def_width, res_def_height) = (res_width, res_height + self.__height // 8)
        resolution_def = small_font.render('WINDOW  MODE', True, self.__white)
        self.__rects['resolution_def_rect'] = resolution_def.get_rect()
        self.__rects['resolution_def_rect'].center = (res_def_width, res_def_height)
        self.__screen.background_surface.blit(resolution_def, self.__rects['resolution_def_rect'])

        (res_2_width, res_2_height) = (res_width, res_def_height + self.__height // 8)
        resolution_2 = small_font.render('FULLSCREEN  MODE', True, self.__white)
        self.__rects['resolution_2_rect'] = resolution_def.get_rect()
        self.__rects['resolution_2_rect'].center = (res_2_width, res_2_height)
        self.__screen.background_surface.blit(resolution_2, self.__rects['resolution_2_rect'])

        pygame.display.update()

    def __win(self):
        self.__level = 1
        self.__state = "win"
        self.__screen.background_surface.fill(self.__black)
        self.__screen.foreground_surface.fill(self.__black)
        self.__music.play_music("win")
        big_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(self.__height * 0.2))
        text = big_font.render('YOU  HAVE  WON', True, self.__white)
        text_rect = text.get_rect()
        text_rect.center = (self.__width // 2, self.__height // 4)
        self.__screen.foreground_surface.blit(text, text_rect)
        self.__screen.update()
        self.__player_spawn, guards = self.__board.load_level()

        return True

    def __game_over(self):
        self.__board.unload()
        self.__level = 1
        self.__state = "game_over"
        self.__screen.background_surface.fill(self.__black)
        self.__screen.foreground_surface.fill(self.__black)
        self.__music.play_music("game_over")
        big_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(self.__height * 0.2))
        text = big_font.render('YOU  HAVE  FAILED', True, self.__white)
        text_rect = text.get_rect()
        text_rect.center = (self.__width // 2, self.__height // 4)
        self.__screen.foreground_surface.blit(text, text_rect)
        self.__screen.update()
        return True

    def move_player(self):
        player_position = self.__player.position()
        if self.__move_counter == 15 // self.__resolution:
            self.__state = 'game'
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
    def move_guards(self):
        for x in range(len(self.__guards)):
            guard_pos = self.__guards[x].position()
            sprites = self.__guards[x].currSprites()
            route = self.__guards[x].route
            step_size = 2 * self.__resolution * self.__resolution
            match route[len(route) % self.__turn_counter]:
                case 'R':
                    # draw background
                    self.__board.draw_level()
                    # draw animation frame
                    if self.__anim_counter % 2 == 0:
                        self.__screen.foreground_surface.blit(self.__guards[x].currSprites()[0], (guard_pos[0],
                                                                                         guard_pos[1]))
                    else:
                        self.__screen.foreground_surface.blit(self.__guards[x].currSprites()[1], (guard_pos[0],
                                                                                                  guard_pos[1]))
                    # slight movement + decrement distance left to travel
                    self.__guards[x].position = (self.__position[0] + step_size, self.__position[1])
                    if not (self.__move_counter % 4):
                        self.__anim_counter += 1

                    # for resetting animation
                    if self.__anim_counter >= len(sprites):
                        self.__anim_counter = 0

                    self.__screen.update()
                    # update player location internally
                case 'L':
                    if self.__board.tiles[guard_pos[1]][guard_pos[0] - 1].type != "w":
                        # draw background
                        self.__board.draw_level()
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
                    if self.__board.tiles[guard_pos[1] - 1][guard_pos[0]].type != "w":
                        # draw background
                        self.__board.draw_level()
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
                    if self.__board.tiles[guard_pos[1] + 1][guard_pos[0]].type != "w":
                        # draw background
                        self.__board.draw_level()
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

            guard_pos = self.__guards[x].position()

            if self.__board.tiles[guard_pos[1]][guard_pos[0]].type == "t" and not \
                    self.__board.tiles[guard_pos[1]][guard_pos[0]].lit:
                self.__board.tiles[guard_pos[1]][guard_pos[0]].unlight()
                self.__board.torch_check()

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
        if self.__board.tiles[player_position[1]][player_position[0]].type == "e":
            return not self.__board.check_for_key()
        return False

    def __check_key(self, player_position):
        if self.__board.tiles[player_position[1]][player_position[0]].type == "k":
            self.__board.tiles[player_position[1]][player_position[0]] = Tile()
            self.__board.torch_check()
            self.__board.unlock()
            return True
        return False

    def __draw_guards(self):
        for x in range(len(self.__guards)):
            self.__guards[x].draw()

    # Runs the actual game
    def __run_game(self):
        self.__board.draw_level()
        self.__player.draw()
        self.__guards[1].draw()
        self.__draw_guards()
        if self.__check_game_over(self.__player.position()):
            self.__game_over()
            self.__player_spawn, self.__guard_routes = self.__get_spawns()
            self.__set_player_and_guards()

        self.__check_key(self.__player.position())  # change to if statement if you want to do hud stuff

        if self.__check_next_level(self.__player.position()):
            if self.__level == 3:
                self.__board.unload()
                self.__win()
                self.__set_player_and_guards()
            else:
                self.__level += 1
                self.__board.unload()
                self.__player_spawn, self.__guard_routes = self.__load_game()
                self.__set_player_and_guards()

    def __update_guards(self):
        for x in range(len(self.__guards)):
            move_direction = self.__guard_routes[x][2][(self.__turn_counter % len(self.__guard_routes[x][2]))]
            self.__board.replace_tile_with_original(self.__guards[x].y, self.__guards[x].x)
            match move_direction:
                case 'R':
                    self.__guards[x].moveRight()
                case 'L':
                    self.__guards[x].moveLeft()
                case 'U':
                    self.__guards[x].moveUp()
                case 'D':
                    self.__guards[x].moveDown()
            self.__board.replace_tile_with_guard(self.__guards[x].y, self.__guards[x].x)

    # Main execution loop
    def run(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        clock = pygame.time.Clock()
        self.__move_counter = 0
        self.__move_flag = False
        while self.__running:
            clock.tick(60)
            self.__move_counter += 1
            if self.__move_counter == 16 // self.__resolution:
                self.__move_counter = 0
            self.__handle_events()
            match self.__state:
                case 'menu':
                    self.__run_menu()
                case 'options':
                    self.__run_options()
                case 'game':
                    if self.__move_flag:
                        self.__update_guards()
                        self.__move_flag = False
                    try:
                        self.__run_game()
                    except Exception as E:
                        print("Attempted to load a game asset but failed (this try/except is in run(self) method):", E)
                case 'game_over':
                    pass
                case 'move':
                    if not self.__move_flag:
                        self.__move_flag = True
                    self.move_player()
            self.__screen.update()
        pygame.quit()
