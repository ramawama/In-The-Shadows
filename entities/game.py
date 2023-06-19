import pygame
from entities.window import Window
from entities.music import Music
from entities.board import Board


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
        text = small_font.render(str(self.__difficulty) + "  MODE  CHOSEN!", True, color)
        text_rect = text.get_rect()
        text_rect.center = (diff_width, hard_height + self.__height // 8)
        self.__screen.background_surface.blit(text, text_rect)
        pygame.display.update()

    # Runs the actual game
    def __run_game(self):
        self.__music.play_music('game')
        self.__board.load_level()
        self.__board.draw_level()
        in_game = True
        while in_game:
            for ev in pygame.event.get():
                match ev.type:
                    case pygame.QUIT:
                        self.__running = False
                        break
                    case pygame.KEYDOWN:
                        match ev.key:
                            case pygame.K_w:
                                moveUp()
                            case pygame.K_a:
                                moveLeft()
                            case pygame.K_s:
                                moveDown()
                            case pygame.K_d:
                                moveRight()
                            case pygame.K_ESCAPE:
                                self.__escape_state()
                                break
                    case pygame.MOUSEBUTTONDOWN:
                        self.__mouse_click(pygame.mouse.get_pos())

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
