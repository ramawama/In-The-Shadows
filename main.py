import pygame


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


def main():
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    (width, height) = (896, 504)
    (start_width, start_height) = (width // 2, height // 2)
    (quit_width, quit_height) = (start_width, start_height + 64)

    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()
    pygame.font.init()
    font = pygame.font.get_default_font()
    font = pygame.font.Font(font, 32)
    text = font.render('IN THE SHADOWS', True, white)
    text_rect = text.get_rect()
    text_rect.center = (width // 2, 32)
    start_text = font.render('START', True, white)
    start_text_rect = start_text.get_rect()
    start_text_rect.center = (start_width, start_height)
    quit_text = font.render('QUIT', True, white)
    quit_rect = pygame.Rect(quit_width, quit_height, 64, 32)
    quit_rect.center = (quit_width - 8, quit_height)

    screen.fill(black)
    square2 = pygame.transform.scale(pygame.Surface((16, 16)), (64, 64))
    square2.fill(red)
    screen.blit(square2, (50, 50))
    screen.blit(text, text_rect)
    screen.blit(start_text, start_text_rect)
    screen.blit(quit_text, quit_rect)

    pygame.mixer.init()
    music = True
    current_music = "menu"
    playMusic(current_music)
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if inButton(mouse, quit_rect):
                    running = False
                elif inButton(mouse, start_text_rect):
                    screen.fill((0, 0, 0, 0))
                    pygame.display.update()
                    startGame(screen, music, width, height)
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_m:
                    if music:
                        pauseMusic()
                        music = False
                    else:
                        playMusic()
                        music = True
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
