import pygame
from pathlib import Path
import time


def game_over(width, height, screen, board):
    pygame.mixer.Sound.play(pygame.mixer.Sound(Path(__file__).parent / "./assets/sounds/death.wav"))
    time.sleep(0.5)
    board.unload()
    level = 1
    state = "game_over"
    game_over_screen = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Game_over_screen.png")
    game_over_screen = pygame.transform.scale(game_over_screen, (width, height))
    screen.foreground_surface.blit(game_over_screen, (0, 0))
    screen.update()
    return level, state


def win(width, height, screen, black, num_torches, num_items, turns_passed):
    level = 1
    state = "win"
    screen.background_surface.fill(black)
    screen.foreground_surface.fill(black)

    background = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Game_win_screen.png")
    background = pygame.transform.scale(background, (width, height))
    font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Minecraftia-Regular.ttf', int(height * 0.05))

    torches_unlit = font.render(str(num_torches), True, (255, 255, 255))
    torches_unlit_rect = torches_unlit.get_rect()
    torches_unlit_rect.x, torches_unlit_rect.y = (7.7 * width // 12, 5.1 * height // 8)

    items_used = font.render(str(num_items), True, (255, 255, 255))
    items_used_rect = items_used.get_rect()
    items_used_rect.x, items_used_rect.y = (7.7 * width // 12, 5.67 * height // 8)

    num_turns = font.render(str(turns_passed), True, (255, 255, 255))
    num_turns_rect = num_turns.get_rect()
    num_turns_rect.x, num_turns_rect.y = (7.7 * width // 12, 6.23 * height // 8)

    screen.foreground_surface.blit(background, (0, 0))
    screen.foreground_surface.blit(torches_unlit, torches_unlit_rect)
    screen.foreground_surface.blit(items_used, items_used_rect)
    screen.foreground_surface.blit(num_turns, num_turns_rect)

    screen.update()
    return level, state
