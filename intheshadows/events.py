import pygame
from pathlib import Path
import time


def game_over(width, height, screen, board):
    pygame.mixer.Sound.play(pygame.mixer.Sound("./assets/sounds/death.wav"))
    time.sleep(0.5)
    board.unload()
    level = 1
    state = "game_over"
    game_over_screen = pygame.image.load(Path(__file__).parent / "assets/graphics/Backgrounds/Game_over_screen.png")
    game_over_screen = pygame.transform.scale(game_over_screen, (width, height))
    screen.foreground_surface.blit(game_over_screen, (0, 0))
    screen.update()
    return level, state


def win(width, height, screen, black, white):
    level = 1
    state = "win"
    screen.background_surface.fill(black)
    screen.foreground_surface.fill(black)
    big_font = pygame.font.Font(Path(__file__).parent / 'assets/fonts/Enchanted Land.otf', int(height * 0.2))
    text = big_font.render('YOU  HAVE  WON', True, white)
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height // 4)
    screen.foreground_surface.blit(text, text_rect)
    screen.update()
    return level, state
