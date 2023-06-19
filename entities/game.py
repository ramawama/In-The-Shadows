import pygame
from entities.window import Window
from entities.music import Music
from entities.board import Board
from entities.player import Player


class Game:
    def __init__(self):
        # Create global variables for height, width, and black and white colors
        self.__black = (0, 0, 0)
        self.__white = (255, 255, 255)
        (self.__width, self.__height) = (896, 504)

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
        self.__board = Board(self.__screen)

        # Load difficulty
        self.__difficulty = "EASY"

    # Changes states when escape is pressed
    def __escape_state(self):
        match self.__state:
            case 'options':
                self.__state = 'menu'
            case 'game':
                self.__state = 'menu'
            case 'menu':
                self.__running = False
            case 'game_over':
                self.__state = 'menu'

    # Changes state based on button click
    def __mouse_click(self, mouse_pos):
        if self.__state == 'menu':
            if self.__rects['start_text_rect'].collidepoint(mouse_pos):
                self.__state = 'game'
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

    # Handles quitting, key presses, and mouse clicks
    def __handle_events(self):
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

        text = big_font.render('IN  THE  SHADOWS', True, self.__white)
        text_rect = text.get_rect()
        text_rect.center = (self.__width // 2, self.__height // 4)

        start_text = small_font.render('START', True, self.__white)
        self.__rects['start_text_rect'] = start_text.get_rect()
        self.__rects['start_text_rect'].center = (start_width, start_height + 1)

        options_text = small_font.render('OPTIONS', True, self.__white)
        self.__rects['options_text_rect'] = options_text.get_rect()
        self.__rects['options_text_rect'].center = (options_width, options_height + options_height // 4)

        quit_text = small_font.render('QUIT', True, self.__white)
        self.__rects['quit_text_rect'] = quit_text.get_rect()
        self.__rects['quit_text_rect'].center = (quit_width, quit_height + quit_height // 4)

        background = pygame.image.load("assets/graphics/Backgrounds/dungeon.jpg")
        background = pygame.transform.scale(background, (self.__width, self.__height))

        self.__screen.background_surface.blit(background, (0, 0))
        self.__screen.background_surface.blit(text, text_rect)
        self.__screen.background_surface.blit(start_text, self.__rects['start_text_rect'])
        self.__screen.background_surface.blit(options_text, self.__rects['options_text_rect'])
        self.__screen.background_surface.blit(quit_text, self.__rects['quit_text_rect'])

    # Runs the options
    def __run_options(self):
        background = pygame.image.load("assets/graphics/Backgrounds/woodBackground.png")
        background = pygame.transform.scale(background, (self.__width, self.__height))
        self.__screen.background_surface.fill(self.__black)
        self.__screen.background_surface.blit(background, (0, 0))

        big_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(self.__height * 0.2))
        small_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(self.__height * 0.09))

        text = big_font.render('OPTIONS', True, self.__white)
        text_rect = text.get_rect()
        (opt_width, opt_height) = (self.__width // 2, self.__height // 8)
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
        pygame.display.update()

    def __game_over(self):
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

    def move_player(self, player, direction):
        # changes sprites depending on if moving left or right (stays the same with up/down)
        if direction == "right" or direction == "left":
            player.direction = direction
        sprites = player.currSprites()
        position = player.position()

        game_over = False

        # parameters for the animation
        distance = 32
        speed = 12
        step_size = 8

        anim_counter = 0
        match direction:
            case "right":
                if self.__board.tiles[(position[1] // 32)][(position[0] // 32) + 1].type != "w":
                    while distance >= 0:
                        pygame.time.Clock().tick(speed)
                        # draw background
                        self.__board.draw_level()
                        # draw animation frame
                        self.__screen.foreground_surface.blit(sprites[anim_counter], (position[0], position[1]))

                        # slight movement + decrement distance left to travel
                        position = (position[0] + step_size, position[1])
                        distance -= step_size
                        anim_counter += 1

                        # for resetting animation
                        if anim_counter >= len(sprites):
                            anim_counter = 0

                        self.__screen.update()
                    # update player location internally
                    player.moveRight()
            case "left":
                if self.__board.tiles[(position[1] // 32)][(position[0] // 32) - 1].type != "w":
                    while distance >= 0:
                        pygame.time.Clock().tick(speed)
                        # draw background
                        self.__board.draw_level()
                        # draw animation frame
                        self.__screen.foreground_surface.blit(sprites[anim_counter], (position[0], position[1]))

                        # slight movement + decrement distance left to travel
                        position = (position[0] - step_size, position[1])
                        distance -= step_size
                        anim_counter += 1

                        # for resetting animation
                        if anim_counter >= len(sprites):
                            anim_counter = 0

                        self.__screen.update()
                    # update player location internally
                    player.moveLeft()
            case "up":
                if self.__board.tiles[(position[1] // 32) - 1][(position[0] // 32)].type != "w":
                    while distance >= 0:
                        pygame.time.Clock().tick(speed)
                        # draw background
                        self.__board.draw_level()
                        # draw animation frame
                        self.__screen.foreground_surface.blit(sprites[anim_counter], (position[0], position[1]))

                        # slight movement + decrement distance left to travel
                        position = (position[0], position[1] - step_size)
                        distance -= step_size
                        anim_counter += 1

                        # for resetting animation
                        if anim_counter >= len(sprites):
                            anim_counter = 0

                        self.__screen.update()
                    # update player location internally
                    player.moveUp()
            case "down":
                if self.__board.tiles[(position[1] // 32) + 1][(position[0] // 32)].type != "w":
                    while distance >= 0:
                        pygame.time.Clock().tick(speed)
                        # draw background
                        self.__board.draw_level()
                        # draw animation frame
                        self.__screen.foreground_surface.blit(sprites[anim_counter], (position[0], position[1]))

                        # slight movement + decrement distance left to travel
                        position = (position[0], position[1] + step_size)
                        distance -= step_size
                        anim_counter += 1

                        # for resetting animation
                        if anim_counter >= len(sprites):
                            anim_counter = 0

                        self.__screen.update()
                    # update player location internally
                    player.moveDown()

        if self.__board.tiles[(position[1] // 32)][(position[0] // 32)].type == "t" and \
                self.__board.tiles[(position[1] // 32)][(position[0] // 32)].lit:
            self.__board.tiles[(position[1] // 32)][(position[0] // 32)].unlight()
            self.__board.torch_check()
        if self.__board.tiles[(position[1] // 32)][(position[0] // 32)].type == "g":
            game_over = self.__game_over()

        # reset clock speed
        pygame.time.Clock().tick(60)
        return game_over

    # Runs the actual game
    def __run_game(self):
        self.__music.play_music('game')
        player_spawn = self.__board.load_level()
        self.__board.draw_level()
        player = Player(self.__screen.foreground_surface, player_spawn[0] * 32, player_spawn[1] * 32)
        in_game = True
        game_over = False
        while in_game:
            self.__board.draw_level()
            player.draw()
            for ev in pygame.event.get():
                match ev.type:
                    case pygame.QUIT:
                        self.__running = False
                        break
                    case pygame.KEYDOWN:
                        match ev.key:
                            case pygame.K_w:
                                game_over = self.move_player(player, "up")
                            case pygame.K_a:
                                game_over = self.move_player(player, "left")
                            case pygame.K_s:
                                game_over = self.move_player(player, "down")
                            case pygame.K_d:
                                game_over = self.move_player(player, "right")
                            case pygame.K_UP:
                                game_over = self.move_player(player, "up")
                            case pygame.K_LEFT:
                                game_over = self.move_player(player, "left")
                            case pygame.K_DOWN:
                                game_over = self.move_player(player, "down")
                            case pygame.K_RIGHT:
                                game_over = self.move_player(player, "right")
                            case pygame.K_ESCAPE:
                                self.__escape_state()
                                in_game = False
                    case pygame.MOUSEBUTTONDOWN:
                        self.__mouse_click(pygame.mouse.get_pos())
            if game_over:
                in_game = False
                for ev in pygame.event.get():
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                        self.__escape_state()
            self.__screen.update()

    # Main execution loop
    def run(self):
        clock = pygame.time.Clock()
        while self.__running:
            clock.tick(60)
            self.__handle_events()
            match self.__state:
                case 'menu':
                    self.__run_menu()
                case 'options':
                    self.__run_options()
                case 'game':
                    self.__run_game()
            self.__screen.update()
        pygame.quit()
