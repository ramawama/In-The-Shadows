import pygame


def settings_menu(screen, width, height):
    background = pygame.image.load("assets/graphics/Backgrounds/woodBackground.png")
    background = pygame.transform.scale(background, (width, height))
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    pygame.display.update()

    font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(height * 0.2))
    small_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(height * 0.09))

    text = font.render('OPTIONS', True, (255, 255, 255))
    text_rect = text.get_rect()
    (opt_width, opt_height) = (width // 2, height // 8)
    text_rect.center = (opt_width, opt_height)
    screen.blit(text, text_rect)

    # display difficulty and controls
    (diff_width, diff_height) = (opt_width // 2, opt_height + height // 6)
    difficulty = small_font.render('SELECT DIFFICULTY', True, (255, 255, 255))
    difficulty_rect = difficulty.get_rect()
    difficulty_rect.center = (diff_width, diff_height)
    screen.blit(difficulty, difficulty_rect)

    (easy_width, easy_height) = (diff_width, diff_height + height // 8)
    easy_difficulty = small_font.render('EASY', True, (0, 153, 0))
    easy_difficulty_rect = easy_difficulty.get_rect()
    easy_difficulty_rect.center = (easy_width, easy_height)
    screen.blit(easy_difficulty, easy_difficulty_rect)

    (med_width, med_height) = (diff_width, easy_height + height // 8)
    medium_difficulty = small_font.render('MEDIUM', True, (255, 128, 0))
    medium_difficulty_rect = medium_difficulty.get_rect()
    medium_difficulty_rect.center = (med_width, med_height)
    screen.blit(medium_difficulty, medium_difficulty_rect)

    (hard_width, hard_height) = (diff_width, med_height + height // 8)
    hard_difficulty = small_font.render('HARD', True, (255, 0, 0))
    hard_difficulty_rect = hard_difficulty.get_rect()
    hard_difficulty_rect.center = (hard_width, hard_height)
    screen.blit(hard_difficulty, hard_difficulty_rect)

    pygame.display.update()
    return easy_difficulty_rect, medium_difficulty_rect, hard_difficulty_rect


def display_difficulty(screen, width, height, diff):
    settings_menu(screen, width, height)
    font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(screen.get_height() * 0.09))
    match diff:
        case "EASY":
            color = (0, 153, 0)
        case "MEDIUM":
            color = (255, 128, 0)
        case "HARD":
            color = (255, 0, 0)
    text = font.render(str(diff) + "  MODE CHOSEN!", True, color)
    text_rect = text.get_rect()
    text_rect.center = (width // 4, height - height // 6)
    screen.blit(text, text_rect)
    pygame.display.update()

