import pygame
from pathlib import Path


def display_help(width, height, resolution, screen):
    # displays controls and instructions while in game by clicking h
    # temp background
    background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/woodBackground_old.png")
    background = pygame.transform.scale(background, (width // 2, height // 2))
    title_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Digital.TTF', int(height * 0.09))
    font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Digital.TTF', int(height * 0.06))

    (title_width, title_height) = (width // 4, height // 16)
    text = title_font.render("HOW TO PLAY", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (title_width, title_height)

    (move_width, move_height) = (title_width // 4, title_height + 48 * resolution)
    move_text = font.render('MOVE:', True, (255, 255, 255))
    move_rect = move_text.get_rect()
    move_rect.center = (move_width, move_height)

    (movement_width, movement_height) = (title_width // 4 + move_width, title_height + 16 * resolution)
    arrow_key = pygame.image.load(
        Path(__file__).parent / "assets/graphics/HUD Elements/arrow_keys.png").convert_alpha()
    scaled_arrow = pygame.transform.scale(arrow_key, (width // 10, height // 10))

    (music_width, music_height) = (movement_width + (4 * resolution), move_height + 48 * resolution)
    music_text = font.render('TOGGLE MUSIC: M', True, (255, 255, 255))
    music_rect = music_text.get_rect()
    music_rect.center = (music_width, music_height)

    (quit_width, quit_height) = (music_width - (16 * resolution), music_height + 48 * resolution)
    quit_text = font.render('QUIT: ESCAPE', True, (255, 255, 255))
    quit_rect = quit_text.get_rect()
    quit_rect.center = (quit_width, quit_height)

    screen.help_surface.blit(background, (0, 0))
    screen.help_surface.blit(text, text_rect)
    screen.help_surface.blit(move_text, move_rect)
    screen.help_surface.blit(scaled_arrow, (movement_width, movement_height))
    screen.help_surface.blit(music_text, music_rect)
    screen.help_surface.blit(quit_text, quit_rect)
    screen.foreground_surface.blit(screen.help_surface, (width // 4, height // 4))


def run_menu(width, height, rects, screen, torch_counter, anim_torches, white):
    if torch_counter % 16 == 0:
        anim_torches = not anim_torches
    screen.background_surface.fill((0, 0, 0))
    screen.foreground_surface.fill((0, 0, 0, 0))
    small_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Enchanted Land.otf', int(height * 0.15))

    (start_width, start_height) = (width // 2, height // 2)
    (options_width, options_height) = (start_width, start_height + start_height // 32)
    (quit_width, quit_height) = (start_width, start_height + start_height // 4)

    start_text = small_font.render('START__', True, white)
    rects['start_text_rect'] = start_text.get_rect()
    rects['start_text_rect'].center = (1.04*start_width, 0.95*start_height)

    options_text = small_font.render('OPTIONS_', True, white)
    rects['options_text_rect'] = options_text.get_rect()
    rects['options_text_rect'].center = (1.02*options_width, options_height + 1.25*options_height // 4)

    quit_text = small_font.render('QUIT__', True, white)
    rects['quit_text_rect'] = quit_text.get_rect()
    rects['quit_text_rect'].center = (1.02*quit_width, quit_height + 1.6*quit_height // 4)

    # animates torches
    if anim_torches:
        background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Home_screen_1.png")
    else:
        background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Home_screen_2.png")
    background = pygame.transform.scale(background, (width, height))

    screen.background_surface.blit(background, (0, 0))
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    if rects['start_text_rect'].collidepoint(mouse_x, mouse_y):
        highlight = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Hover Text/start.png")
        highlight = pygame.transform.scale(highlight, (width, height))
        screen.background_surface.blit(highlight, (0, 0))
    if rects['options_text_rect'].collidepoint(mouse_x, mouse_y):
        highlight = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Hover Text/options.png")
        highlight = pygame.transform.scale(highlight, (width, height))
        screen.background_surface.blit(highlight, (0, 0))
    if rects['quit_text_rect'].collidepoint(mouse_x, mouse_y):
        highlight = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Hover Text/quit.png")
        highlight = pygame.transform.scale(highlight, (width, height))
        screen.background_surface.blit(highlight, (0, 0))


def run_options(width, height, rects, screen, torch_counter, anim_torches, black, white, difficulty):
    if torch_counter % 8 == 0:
        anim_torches = not anim_torches

    # animates torches
    if anim_torches:
        background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_1.png")
    else:
        background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_2.png")
    background = pygame.transform.scale(background, (width, height))

    screen.background_surface.fill(black)
    screen.background_surface.blit(background, (0, 0))

    big_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Enchanted Land.otf', int(height * 0.2))
    small_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Enchanted Land.otf', int(height * 0.09))

    (opt_width, opt_height) = (width // 2, height // 8)
    text = big_font.render('OPTIONS', True, white)
    text_rect = text.get_rect()
    text_rect.center = (opt_width, opt_height)
    # screen.background_surface.blit(text, text_rect)

    (diff_width, diff_height) = (opt_width // 2, opt_height + height // 6)

    # back button
    rects['options_back_button'] = pygame.Rect((0.05*width, 0.06*height), (0.08*width, 0.09*height))

    (easy_width, easy_height) = (diff_width, diff_height + height // 8)
    easy_difficulty = small_font.render('EASY_', True, (0, 153, 0))
    rects['easy_difficulty_rect'] = easy_difficulty.get_rect()
    rects['easy_difficulty_rect'].center = (easy_width, easy_height)

    (med_width, med_height) = (diff_width, easy_height + 1.27*height // 8)
    medium_difficulty = small_font.render('_MEDIUM_', True, (255, 128, 0))
    rects['medium_difficulty_rect'] = medium_difficulty.get_rect()
    rects['medium_difficulty_rect'].center = (med_width, med_height)

    (hard_width, hard_height) = (diff_width, med_height + 1.30*height // 8)
    hard_difficulty = small_font.render('HARD_', True, (255, 0, 0))
    rects['hard_difficulty_rect'] = hard_difficulty.get_rect()
    rects['hard_difficulty_rect'].center = (hard_width, hard_height)

    match difficulty:
        case "EASY":
            mode = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_easy.png")
            # color = (0, 153, 0)
        case "MEDIUM":
            mode = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_medium.png")
            # color = (255, 128, 0)
        case "HARD":
            mode = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_hard.png")
            # color = (255, 0, 0)
        case _:
            mode = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_easy.png")
            # color = (255, 255, 255)
    mode = pygame.transform.scale(mode, (width, height))
    screen.background_surface.blit(mode, (0, 0))

    (res_width, res_height) = (width - width // 4, opt_height + height // 6)

    (res_def_width, res_def_height) = (res_width, res_height + height // 8)
    resolution_def = small_font.render('_WINDOW_', True, (255, 0, 0))
    rects['resolution_def_rect'] = resolution_def.get_rect()
    rects['resolution_def_rect'].center = (1.02*res_def_width, res_def_height)
    # screen.background_surface.blit(resolution_def, rects['resolution_def_rect'])

    (res_2_width, res_2_height) = (res_width, res_def_height + height // 8)
    resolution_2 = small_font.render('00__FULLSCREEN_0', True, (255, 0, 0))
    rects['resolution_2_rect'] = resolution_def.get_rect()
    rects['resolution_2_rect'].center = (0.93*res_2_width, 1.07*res_2_height)
    # screen.background_surface.blit(resolution_2, rects['resolution_2_rect'])

    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    if rects['resolution_def_rect'].collidepoint(mouse_x, mouse_y):
        highlight = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Hover Text/window.png")
        highlight = pygame.transform.scale(highlight, (width, height))
        screen.background_surface.blit(highlight, (0, 0))
    if rects['resolution_2_rect'].collidepoint(mouse_x, mouse_y):
        highlight = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Hover Text/fullscreen.png")
        highlight = pygame.transform.scale(highlight, (width, height))
        screen.background_surface.blit(highlight, (0, 0))
    if rects['easy_difficulty_rect'].collidepoint(mouse_x, mouse_y):
        highlight = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Hover Text/easy.png")
        highlight = pygame.transform.scale(highlight, (width, height))
        screen.background_surface.blit(highlight, (0, 0))
    if rects['medium_difficulty_rect'].collidepoint(mouse_x, mouse_y):
        highlight = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Hover Text/medium.png")
        highlight = pygame.transform.scale(highlight, (width, height))
        screen.background_surface.blit(highlight, (0, 0))
    if rects['hard_difficulty_rect'].collidepoint(mouse_x, mouse_y):
        highlight = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Hover Text/hard.png")
        highlight = pygame.transform.scale(highlight, (width, height))
        screen.background_surface.blit(highlight, (0, 0))
    if rects['options_back_button'].collidepoint(mouse_x, mouse_y):
        highlight = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Hover Text/back_arrow.png")
        highlight = pygame.transform.scale(highlight, (width, height))
        screen.background_surface.blit(highlight, (0, 0))