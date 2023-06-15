import pygame


def settings_menu(screen, width, height):
    diff = "easy"

    background = pygame.image.load("assets/graphics/Backgrounds/woodBackground.png")
    background = pygame.transform.scale(background, (width, height))
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    pygame.display.update()

    font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(height * 0.2))
    small_font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(height * 0.10))

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
    easy_difficulty = small_font.render('EASY', True, (255, 255, 255))
    easy_difficulty_rect = easy_difficulty.get_rect()
    easy_difficulty_rect.center = (easy_width, easy_height)
    screen.blit(easy_difficulty, easy_difficulty_rect)

    (med_width, med_height) = (diff_width, easy_height + height // 8)
    medium_difficulty = small_font.render('MEDIUM', True, (255, 255, 255))
    medium_difficulty_rect = medium_difficulty.get_rect()
    medium_difficulty_rect.center = (med_width, med_height)
    screen.blit(medium_difficulty, medium_difficulty_rect)

    (hard_width, hard_height) = (diff_width, med_height + height // 8)
    hard_difficulty = small_font.render('HARD', True, (255, 255, 255))
    hard_difficulty_rect = hard_difficulty.get_rect()
    hard_difficulty_rect.center = (hard_width, hard_height)
    screen.blit(hard_difficulty, hard_difficulty_rect)

    pygame.display.update()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop and stop the options menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if in_button(pos, easy_difficulty_rect):
                    diff = "easy"
                    display_difficulty(screen, width, height, diff)
                if in_button(pos, medium_difficulty_rect):
                    diff = "medium"
                    display_difficulty(screen, width, height, diff)
                if in_button(pos, hard_difficulty_rect):
                    diff = "hard"
                    display_difficulty(screen, width, height, diff)

        pygame.display.update()

    return diff


def display_difficulty(screen, width, height, diff):
    font = pygame.font.Font('assets/fonts/Enchanted Land.otf', int(screen.get_height() * 0.10))
    text = font.render(diff + " MODE CHOSEN!", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height - height // 2)
    screen.blit(text, text_rect)
    pygame.display.update()


def in_button(pos, button):  # pass in pygame.mouse.get_pos() and the "square" surface object
    if button.collidepoint(pos):
        return True
    else:
        return False
