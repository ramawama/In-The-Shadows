import pygame


def inButton(pos, button):  # pass in pygame.mouse.get_pos() and the "square" surface object
    if button.get_rect().collidepoint(pos):
        return True
    else:
        return False


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
    text = font.render('IN THE SHADOWS', True, black)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)

    while True:
        screen.fill(white)
        square2 = pygame.transform.scale(pygame.Surface((16, 16)), (64, 64))
        square2.fill(red)
        square2.get_rect().collidepoint()
        screen.blit(square2, (50, 50))
        screen.blit(text, textRect)
        pygame.display.update()
        pass


if __name__ == "__main__":
    main()
