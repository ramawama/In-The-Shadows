import pygame
from pathlib import Path


def display_help(width, height, resolution, screen):
    # displays controls and instructions while in game by clicking h
    # temp background
    background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/woodBackground_old.png")
    background = pygame.transform.scale(background, (width // 2, height // 2))
    title_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf', int(height * 0.09))
    font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf', int(height * 0.06))

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


def display_inventory(width, height, resolution, screen, player):
    background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/dungeon_old.jpg")
    background = pygame.transform.scale(background, (width // 2, height // 2))
    title_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf', int(height * 0.09))
    font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf', int(height * 0.06))

    (title_width, title_height) = (width // 4, height // 16)
    text = title_font.render("INVENTORY", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (title_width, title_height)

    if player.dash_cooldown == 0:
        dash_text = font.render('SPACE TO DASH', True, (255, 255, 255))
        (dash_width, dash_height) = (title_width - 128 * resolution, title_height + 48 * resolution)
    else:
        dash_text = font.render('DASH COOLDOWN: ' + str(player.dash_cooldown), True, (255, 255, 255))
        (dash_width, dash_height) = (title_width - 96 * resolution, title_height + 48 * resolution)

    dash_rect = dash_text.get_rect()
    dash_rect.center = (dash_width, dash_height)

    screen.help_surface.blit(background, (0, 0))
    screen.help_surface.blit(text, text_rect)
    screen.help_surface.blit(dash_text, dash_rect)
    screen.foreground_surface.blit(screen.help_surface, (width // 4, height // 4))


def run_menu(width, height, rects, screen, anim_torches):
    # animates torches
    if anim_torches:
        background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Home_screen_1.png")
    else:
        background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Home_screen_2.png")
    background = pygame.transform.scale(background, (width, height))
    screen.background_surface.fill((0, 0, 0))
    screen.foreground_surface.fill((0, 0, 0, 0))

    # rects for collision
    rects['start_text_rect'] = pygame.Rect((0.39 * width, 0.43 * height), (0.25 * width, 0.1 * height))
    rects['options_text_rect'] = pygame.Rect((0.35 * width, 0.64 * height), (0.32 * width, 0.1 * height))
    rects['quit_text_rect'] = pygame.Rect((0.42 * width, 0.82 * height), (0.20 * width, 0.11 * height))
    screen.background_surface.blit(background, (0, 0))

    # highlight text when hovering
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


def run_options(width, height, rects, screen, anim_torches, difficulty):
    # animates torches
    if anim_torches:
        background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_1.png")
    else:
        background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_2.png")
    background = pygame.transform.scale(background, (width, height))
    screen.background_surface.fill((255, 255, 255))
    screen.background_surface.blit(background, (0, 0))

    # rects for collision
    rects['options_back_button'] = pygame.Rect((0.05 * width, 0.06 * height), (0.08 * width, 0.09 * height))
    rects['easy_difficulty_rect'] = pygame.Rect((0.17 * width, 0.37 * height), (0.16 * width, 0.09 * height))
    rects['medium_difficulty_rect'] = pygame.Rect((0.14 * width, 0.53 * height), (0.22 * width, 0.09 * height))
    rects['hard_difficulty_rect'] = pygame.Rect((0.17 * width, 0.7 * height), (0.16 * width, 0.09 * height))
    rects['resolution_def_rect'] = pygame.Rect((0.66 * width, 0.37 * height), (0.21 * width, 0.09 * height))
    rects['resolution_2_rect'] = pygame.Rect((0.59 * width, 0.53 * height), (0.35 * width, 0.09 * height))

    # update difficulty
    match difficulty:
        case "EASY":
            mode = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_easy.png")
        case "MEDIUM":
            mode = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_medium.png")
        case "HARD":
            mode = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_hard.png")
        case _:
            mode = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Options_easy.png")
    mode = pygame.transform.scale(mode, (width, height))
    screen.background_surface.blit(mode, (0, 0))

    # highlight text when hovering
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


def loading_screen(width, height, resolution, screen, level):
    screen.foreground_surface.fill((0, 0, 0))
    pre_game_screen = pygame.transform.scale(pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Pre_game_screen.png"), (width, height))
    title_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf', int(height * 0.06))
    font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf', int(height * 0.06))

    # (title_width, title_height) = (width // 2, height // 8)
    # title = title_font.render("LOADING...", True, (255, 255, 255))
    # title_rect = title.get_rect()
    # title_rect.center = (title_width, title_height)
    #
    # (level_width, level_height) = (width - 192 * resolution, title_height + 64 * resolution)
    curr_level = font.render(str(level), True, (255, 255, 255))
    curr_level_rect = curr_level.get_rect()
    curr_level_rect.center = (10 * width // 11, 1.2 * height // 8)

    # (restart_width, restart_height) = (width - 192 * resolution, level_height + 64 * resolution)
    # restart = font.render("Click R to Restart", True, (255, 255, 255))
    # restart_rect = restart.get_rect()
    # restart_rect.center = (restart_width, restart_height)
    #
    # (exit_width, exit_height) = (width // 2, height - height // 8)
    # exit = font.render("PRESS OR CLICK TO CONTINUE", True, (255, 255, 255))
    # exit_rect = exit.get_rect()
    # exit_rect.center = (exit_width, exit_height)
    #
    # (howto_width, howto_height) = (title_width // 2 - 32 * resolution, title_height + 64 * resolution)
    # howto = font.render("HOW TO PLAY:", True, (255, 255, 255))
    # howto_rect = howto.get_rect()
    # howto_rect.center = (howto_width, howto_height)

    # (move_width, move_height) = (title_width // 4, howto_height + 48 * resolution)
    # move_text = font.render('MOVE:', True, (255, 255, 255))
    # move_rect = move_text.get_rect()
    # move_rect.center = (move_width, move_height)
    #
    # (movement_width, movement_height) = (title_width // 4 + move_width, howto_height + 16 * resolution)
    # arrow_key = pygame.image.load(
    #     Path(__file__).parent / "assets/graphics/HUD Elements/arrow_keys.png").convert_alpha()
    # scaled_arrow = pygame.transform.scale(arrow_key, (width // 10, height // 10))
    #
    # (music_width, music_height) = (movement_width + (4 * resolution), move_height + 48 * resolution)
    # music_text = font.render('TOGGLE MUSIC: M', True, (255, 255, 255))
    # music_rect = music_text.get_rect()
    # music_rect.center = (music_width, music_height)
    #
    # (quit_width, quit_height) = (music_width - (16 * resolution), music_height + 48 * resolution)
    # quit_text = font.render('QUIT: ESCAPE', True, (255, 255, 255))
    # quit_rect = quit_text.get_rect()
    # quit_rect.center = (quit_width, quit_height)

    screen.foreground_surface.blit(pre_game_screen, (0, 0))
    # screen.foreground_surface.blit(title, title_rect)
    # screen.foreground_surface.blit(howto, howto_rect)
    screen.foreground_surface.blit(curr_level, curr_level_rect)
    # screen.foreground_surface.blit(restart, restart_rect)
    # screen.foreground_surface.blit(exit, exit_rect)
    # screen.foreground_surface.blit(move_text, move_rect)
    # screen.foreground_surface.blit(scaled_arrow, (movement_width, movement_height))
    # screen.foreground_surface.blit(music_text, music_rect)
    # screen.foreground_surface.blit(quit_text, quit_rect)






