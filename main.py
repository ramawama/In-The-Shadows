import pygame
from entities.tile import Tile
from entities.player import Player
import options


def in_button(pos, button):  # pass in pygame.mouse.get_pos() and the "square" surface object
    if button.collidepoint(pos):
        return True
    else:
        return False


def play_music(choice="unpause"):
    if choice == 'menu':
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("./assets/sounds/menu.wav")
        pygame.mixer.music.play(-1)
    elif choice == 'game':
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("./assets/sounds/game.wav")
        pygame.mixer.music.play(-1)
    elif choice == 'game_over':
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("./assets/sounds/game_over.wav")
        pygame.mixer.music.play(-1)
    elif choice == 'unpause':
        pygame.mixer.music.unpause()
    else:
        print("Unexpected music input! Playing game music")
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("game.wav")
        pygame.mixer.music.play(-1)


def pause_music():
    pygame.mixer.music.pause()


def analyze_level(level):
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col].type == "t":
                level[row + 1][col].light()
                level[row + 1][col - 1].light()
                level[row + 1][col + 1].light()
                level[row - 1][col].light()
                level[row - 1][col - 1].light()
                level[row - 1][col + 1].light()
                level[row][col - 1].light()
                level[row][col + 1].light()

    return level


def load_level(name="level_TEST"):
    try:
        with open("./levels/" + name, "r") as file:
            file.readline().strip()  # this is the level name if you want it
            tile_array = []
            for line in file:
                row_array = []
                for char in line.strip():
                    row_array.append(Tile(char))
                tile_array.append(row_array)
            file.close()
            tile_array = analyze_level(tile_array)
            return tile_array, None

    except IOError:
        print("Error from loadLevel function!")


def draw_level(level, screen, width, height):
    screen.fill((0, 0, 0))
    pygame.display.update()

    rows = len(level)
    cols = len(level[0])

    tile_width = width // cols
    tile_height = height // rows

    for row in range(rows):
        for col in range(cols):
            tile_x = col * tile_width
            tile_y = row * tile_height

            scaled_tile_image = pygame.transform.scale(level[row][col].image, (tile_width, tile_height))
            if level[row][col].type != "o":
                if level[row][col].lit:
                    scaled_floor_image = pygame.transform.scale(Tile("o", True).image, (tile_width, tile_height))
                else:
                    scaled_floor_image = pygame.transform.scale(Tile().image, (tile_width, tile_height))
                screen.blit(scaled_floor_image, (tile_x, tile_y))

            screen.blit(scaled_tile_image, (tile_x, tile_y))

    pygame.display.update()


def start_game(screen, music, width, height):
    screen.fill((0, 0, 0))
    pygame.display.update()

    if music:
        play_music("game")

    font = pygame.font.get_default_font()
    font = pygame.font.Font(font, 32)
    text = font.render('LOADING LEVEL...', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(text, text_rect)

    pygame.display.update()

    level, guard_routes = load_level()
    """
    note: my idea for guard movement is after the map data in the level text documents, 
    for each guard we should define their starting position and default patrol routes.
    guard route should be formatted as a tuple with guard_route[0] being the
    starting position (will be updated with guard's current position during game loop)
    and guard_route[1] should be an array of the guard's routes in direction form
    (i.e. UUDD for up up down down)
    then we can use modulo to iterate through this array on a looping basis
    """
    draw_level(level, screen, width, height)
    # play_level(level, guard_routes)


def play_level(game_board, guard_routes):
    player = Player()  # create player asset
    turn_counter = 1
    current_x, current_y, exit_x, exit_y = -1
    for y in game_board:
        for x in y:
            if game_board[y][x] == 's':
                current_x = x
                current_y = y
            if game_board[y][x] == 'e':
                exit_x = x
                exit_y = y
    if current_x == -1:
        raise IOError("Imported level does not contain a starting point")
    if exit_x == -1:
        raise IOError("Imported level does not contain an exit point")
    guard_status = check_guard_status()
    while True:
        current_x, current_y, player = move(game_board, current_x, current_y, player)
        if current_x == exit_x and current_y == exit_y:  # player reached exit tile
            # you can add a condition like need key here or something
            break
        guard_status = check_guard_status()
        enemy_move()
        turn_counter = turn_counter + 1
        guard_status = check_guard_status()


def check_guard_status():
    return "Passive"


def is_wall(game_board, x, y):
    return game_board[x][y] == 'W'


def move(game_board, current_x, current_y, player):
    while True:
        ev = pygame.event.get()
        match ev.type:
            case pygame.KEYDOWN:
                match ev.key:
                    case pygame.K_w | pygame.K_UP:
                        if not is_wall(game_board, current_x, current_y - 1):
                            player.direction = "up"
                            # redraw player here
                            return current_x, current_y - 1
                        else:
                            print("THIS GUYT RIED TO WALK INTO A WALL!!!")
                    case pygame.K_a | pygame.K_LEFT:
                        if not is_wall(game_board, current_x - 1, current_y):
                            player.direction = "left"
                            return current_x - 1, current_y
                        else:
                            print("THIS GUYT RIED TO WALK INTO A WALL!!!")
                    case pygame.K_s | pygame.K_DOWN:
                        if not is_wall(game_board, current_x, current_y + 1):
                            player.direction = "down"
                            return current_x, current_y + 1
                        else:
                            print("THIS GUYT RIED TO WALK INTO A WALL!!!")
                    case pygame.K_d | pygame.K_RIGHT:
                        if not is_wall(game_board, current_x + 1, current_y):
                            player.direction = "right"
                            return current_x + 1, current_y
                        else:
                            print("THIS GUYT RIED TO WALK INTO A WALL!!!")


def enemy_move():
    return None


def drawMenu(width=896, height=504):
    white = (255, 255, 255)
    black = (0, 0, 0)
    (start_width, start_height) = (width // 2, height // 2)
    (options_width, options_height) = (start_width, start_height + start_height // 32)
    (quit_width, quit_height) = (start_width, start_height + start_height // 4)
    real_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    screen = real_screen.copy()
    screen.fill(black)
    pygame.display.flip()

    pygame.font.init()
    big_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(height * 0.2))
    small_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(height * 0.15))

    text = big_font.render('IN  THE  SHADOWS', True, white)

    text_rect = text.get_rect()
    text_rect.center = (width // 2, height // 4)
    start_text = small_font.render('START', True, white)
    start_text_rect = start_text.get_rect()
    start_text_rect.center = (start_width,
                              start_height + 1)  # had to add one or there will be a gap between options and no gap between quit and options
    options_text = small_font.render('OPTIONS', True, white)
    options_text_rect = options_text.get_rect()
    options_text_rect.center = (options_width, options_height + options_height // 4)
    quit_text = small_font.render('QUIT', True, white)
    quit_text_rect = quit_text.get_rect()
    quit_text_rect.center = (quit_width, quit_height + quit_height // 4)

    background = pygame.image.load("assets/graphics/Backgrounds/dungeon.jpg")
    background = pygame.transform.scale(background, (width, height))

    screen.fill(black)
    screen.blit(background, (0, 0))

    screen.blit(text, text_rect)
    screen.blit(start_text, start_text_rect)
    screen.blit(options_text, options_text_rect)
    screen.blit(quit_text, quit_text_rect)

    return real_screen, screen, quit_text_rect, start_text_rect, options_text_rect


def main():
    real_screen, screen, quit_text_rect, start_text_rect, options_text_rect = drawMenu()

    pygame.display.set_caption("In the Shadows")

    music = True
    pygame.mixer.init()
    current_music = "menu"
    play_music(current_music)

    running = True
    screen_state = "menu"
    while running:
        real_screen.blit(pygame.transform.scale(screen, real_screen.get_rect().size), (0, 0))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if in_button(mouse, quit_text_rect):
                    running = False
                elif in_button(mouse, start_text_rect):
                    screen_state = "game"
                    screen.fill((0, 0, 0, 0))
                    pygame.display.update()
                    start_game(screen, music, real_screen.get_width(), real_screen.get_height())
                elif in_button(mouse, options_text_rect):
                    screen_state = "options"
                    screen.fill((0, 0, 0, 0))
                    pygame.display.update()
                    easy_rect, med_rect, hard_rect = options.settings_menu(screen, real_screen.get_width(), real_screen.get_height())
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_m:
                    if music:
                        pause_music()
                        music = False
                    else:
                        play_music()
                        music = True
                if ev.key == pygame.K_ESCAPE:
                    if screen_state == 'options':
                        screen_state = "menu"
                        real_screen, screen, quit_text_rect, start_text_rect, options_text_rect = drawMenu(
                            real_screen.get_width(), real_screen.get_height())
                    elif screen_state == 'game':
                        screen_state = 'menu'
                        play_music("menu")
                        real_screen, screen, quit_text_rect, start_text_rect, options_text_rect = drawMenu(
                            real_screen.get_width(), real_screen.get_height())
            elif ev.type == pygame.VIDEORESIZE:
                real_screen = pygame.display.set_mode(ev.size, pygame.RESIZABLE)
                match screen_state:
                    case "menu":
                        real_screen, screen, quit_text_rect, start_text_rect, options_text_rect = drawMenu(
                            real_screen.get_width(), real_screen.get_height())
                    case "options":
                        easy_rect, med_rect, hard_rect = options.settings_menu(real_screen, real_screen.get_width(),
                                                                               real_screen.get_height())

                        # test options menu later with inputs
                    case "game":
                        pass
                        # startGame(real_screen, music, real_screen.get_width(), real_screen.get_height())
                        # just reloads game with new size, will prob be issue later

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
