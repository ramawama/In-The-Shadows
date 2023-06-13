import pygame
import sys

def main():
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    (width, height) = (896, 504)

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
    start_text_rect.center = (width // 2, height // 2)


    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                    pygame.quit()

        screen.fill(black)
        mouse = pygame.mouse.get_pos()
        square2 = pygame.transform.scale(pygame.Surface((16, 16)), (64, 64))
        square2.fill(red)
        screen.blit(square2, (50, 50))
        screen.blit(text, textRect)
        screen.blit(start_text, start_text_rect)
        pygame.display.update()
        pass


if __name__ == "__main__":
    main()
