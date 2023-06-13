import pygame


def main():
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    (width, height) = (896, 504)
    (start_width, start_height) = (width // 2, height // 2)
    (quit_width, quit_height) = (start_width , start_height + 64)

    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()
    pygame.font.init()
    font = pygame.font.get_default_font()
    font = pygame.font.Font(font, 32)
    text = font.render('IN THE SHADOWS', True, white)
    textRect = text.get_rect()
    textRect.center = (width // 2, 32)
    start_text = font.render('START', True, white)
    start_text_rect = start_text.get_rect()
    start_text_rect.center = (start_width, start_height)
    quit_text = font.render('QUIT', True, white)
    quit_rect = pygame.Rect(quit_width, quit_height, 64, 32)
    quit_rect.center = (quit_width - 8, quit_height)


    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # if left-clicked
                if quit_width - 64 <= mouse[0] <= quit_width and quit_height <= mouse[1] <= quit_height + 32:
                    pygame.quit()

        screen.fill(black)
        mouse = pygame.mouse.get_pos()
        square2 = pygame.transform.scale(pygame.Surface((16, 16)), (64, 64))
        square2.fill(red)
        screen.blit(square2, (50, 50))
        screen.blit(text, textRect)
        screen.blit(start_text, start_text_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.update()



if __name__ == "__main__":
    main()
