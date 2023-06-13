import pygame
from pygame import Surface


def inButton(pos, button):  # pass in pygame.mouse.get_pos() and the "square" surface object
    if button.collidepoint(pos):
        return True
    else:
        return False


def playMusic(choice="unpause"):
    if choice == 'menu':
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("./assets/sounds/menu.wav")
        pygame.mixer.music.play(-1)
    elif choice == 'game':
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("./assets/sounds/game.wav")
        pygame.mixer.music.play(-1)
    elif choice == 'game_over':
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("./assets/sounds/game_over.wav")
        pygame.mixer.music.play(-1)
    elif choice == 'unpause':
        pygame.mixer.music.unpause()
    else:
        print("Unexpected music input! Playing game music")
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("game.wav")
        pygame.mixer.music.play(-1)


def pauseMusic():
    pygame.mixer.music.pause()


def startGame(screen, music, width, height):
    screen.fill((0, 0, 0))
    pygame.display.update()

    if music:
        playMusic("game")

    font = pygame.font.get_default_font()
    font = pygame.font.Font(font, 32)
    text = font.render('LOADING LEVEL...', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(text, text_rect)

    pygame.display.update()
    # TODO: make a load level function
    # loadLevel()


def drawMenu(width=896, height=504):

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    (start_width, start_height) = (width // 2, height // 2)
    (quit_width, quit_height) = (start_width, start_height + start_height // 4)
    real_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    screen = real_screen.copy()
    screen.fill(black)
    pygame.display.flip()
    pygame.font.init()
    font = pygame.font.get_default_font()
    font = pygame.font.Font(font, 90)
    text = font.render('IN THE SHADOWS', True, white)
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height // 4)
    font = pygame.font.get_default_font()
    font = pygame.font.Font(font, 70)
    start_text = font.render('START', True, white)
    start_text_rect = start_text.get_rect()
    start_text_rect.center = (start_width, start_height)
    quit_text = font.render('QUIT', True, white)
    quit_text_rect = quit_text.get_rect()
    quit_text_rect.center = (quit_width, quit_height + quit_height // 4)

    background = pygame.image.load("./assets/graphics/background.png")
    background = pygame.transform.scale(background, (width, height))

    screen.fill(black)
    screen.blit(background, (0, 0))
    # square2 = pygame.transform.scale(pygame.Surface((16, 16)), (64, 64))
    # square2.fill(red)
    # screen.blit(square2, (50, 50))

    image = Surface(text_rect.size)
    image.fill(black, text_rect)
    screen.blit(image, (text_rect.x, text_rect.y))

    image2 = Surface(start_text_rect.size)
    image2.fill(black, start_text_rect)
    screen.blit(image2, (start_text_rect.x, start_text_rect.y))

    image3 = Surface(quit_text_rect.size)
    image3.fill(black, quit_text_rect)
    screen.blit(image3, (quit_text_rect.x, quit_text_rect.y))

    screen.blit(text, text_rect)
    screen.blit(start_text, start_text_rect)
    screen.blit(quit_text, quit_text_rect)

    return real_screen, screen, quit_text_rect, start_text_rect

def main():

    real_screen, screen, quit_text_rect, start_text_rect = drawMenu()

    pygame.display.set_caption("In the Shadows")
    pygame.mixer.init()
    music = True
    current_music = "menu"
    playMusic(current_music)
    running = True
    while running:
        real_screen.blit(pygame.transform.scale(screen, real_screen.get_rect().size), (0, 0))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if inButton(mouse, quit_text_rect):
                    running = False
                elif inButton(mouse, start_text_rect):
                    screen.fill((0, 0, 0, 0))
                    pygame.display.update()
                    startGame(screen, music, real_screen.get_width(), real_screen.get_height())
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_m:
                    if music:
                        pauseMusic()
                        music = False
                    else:
                        playMusic()
                        music = True
            elif ev.type == pygame.VIDEORESIZE:
                real_screen = pygame.display.set_mode(ev.size, pygame.RESIZABLE)
                real_screen, screen, quit_text_rect, start_text_rect = drawMenu(real_screen.get_width(), real_screen.get_height())
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
