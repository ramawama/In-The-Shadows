import pygame
from pathlib import Path


def display_info(width, height, screen, level, num_torches, num_items, turns_passed, num_bottles, num_bombs):
    background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Info_screen.png")
    background = pygame.transform.scale(background, (width // 2, height // 2))
    font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf', int(height // 2 * 0.05))

    curr_level = font.render(str(level), True, (255, 255, 255))
    curr_level_rect = curr_level.get_rect()
    curr_level_rect.x, curr_level_rect.y = (9.9 * width // 11 // 2, 0.91 * height // 8 // 2)

    torches_unlit = font.render(str(num_torches), True, (255, 255, 255))
    torches_unlit_rect = torches_unlit.get_rect()
    torches_unlit_rect.x, torches_unlit_rect.y = (9.9 * width // 11 // 2, 1.44 * height // 8 // 2)

    items_used = font.render(str(num_items), True, (255, 255, 255))
    items_used_rect = items_used.get_rect()
    items_used_rect.x, items_used_rect.y = (9.18 * width // 11 // 2, 1.98 * height // 8 // 2)

    num_turns = font.render(str(turns_passed), True, (255, 255, 255))
    num_turns_rect = num_turns.get_rect()
    num_turns_rect.x, num_turns_rect.y = (9.65 * width // 11 // 2, 2.51 * height // 8 // 2)

    num_water_bottles = font.render(str(num_bottles), True, (255, 255, 255))
    num_water_bottles_rect = num_water_bottles.get_rect()
    num_water_bottles_rect.x, num_water_bottles_rect.y = (8.75 * width // 11 // 2, 4.68 * height // 8 // 2)

    num_smoke_bombs = font.render(str(num_bombs), True, (255, 255, 255))
    num_smoke_bombs_rect = num_smoke_bombs.get_rect()
    num_smoke_bombs_rect.x, num_smoke_bombs_rect.y = (8.75 * width // 11 // 2, 5.68 * height // 8 // 2)

    screen.help_surface.blit(background, (0, 0))
    screen.help_surface.blit(curr_level, curr_level_rect)
    screen.help_surface.blit(torches_unlit, torches_unlit_rect)
    screen.help_surface.blit(items_used, items_used_rect)
    screen.help_surface.blit(num_turns, num_turns_rect)
    screen.help_surface.blit(num_water_bottles, num_water_bottles_rect)
    screen.help_surface.blit(num_smoke_bombs, num_smoke_bombs_rect)
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


def loading_screen(width, height, screen, level, num_torches, num_items, turns_passed):
    screen.foreground_surface.fill((0, 0, 0))
    pre_game_screen = pygame.transform.scale(
        pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Pre_game_screen.png"), (width, height))
    font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf', int(height * 0.045))

    curr_level = font.render(str(level), True, (255, 255, 255))
    curr_level_rect = curr_level.get_rect()
    curr_level_rect.x, curr_level_rect.y = (9.9 * width // 11, 0.95 * height // 8)

    torches_unlit = font.render(str(num_torches), True, (255, 255, 255))
    torches_unlit_rect = torches_unlit.get_rect()
    torches_unlit_rect.x, torches_unlit_rect.y = (9.9 * width // 11, 1.48 * height // 8)

    items_used = font.render(str(num_items), True, (255, 255, 255))
    items_used_rect = items_used.get_rect()
    items_used_rect.x, items_used_rect.y = (9.18 * width // 11, 2.02 * height // 8)

    num_turns = font.render(str(turns_passed), True, (255, 255, 255))
    num_turns_rect = num_turns.get_rect()
    num_turns_rect.x, num_turns_rect.y = (9.65 * width // 11, 2.55 * height // 8)

    screen.foreground_surface.blit(pre_game_screen, (0, 0))
    screen.foreground_surface.blit(curr_level, curr_level_rect)
    screen.foreground_surface.blit(torches_unlit, torches_unlit_rect)
    screen.foreground_surface.blit(items_used, items_used_rect)
    screen.foreground_surface.blit(num_turns, num_turns_rect)
