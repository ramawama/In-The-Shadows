import pygame


def moveRight(screen, x, y, rogue, background, speed):
    distance = 32
    anim_counter = 0
    tile_x = x
    tile_y = y
    while True:
        # draw background
        screen.blit(background, (tile_x, tile_y))
        if distance - 16 <= 0:
            screen.blit(background, (tile_x + 32, tile_y))
        pygame.time.Clock().tick(speed)

        screen.blit(rogue[anim_counter], (x, y))
        x += 4
        distance -= 4
        anim_counter += 1

        if anim_counter >= len(rogue):
            anim_counter = 0

        if distance <= 0:
            return x, y

        pygame.display.update()


def main():
    white = (255, 255, 255)
    (width, height) = (896, 504)

    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()
    pygame.font.init()

    torch = [pygame.image.load("assets/graphics/Level Elements/Torch/Torch_small.png"),
             pygame.image.load("assets/graphics/Level Elements/Torch/Torch_big.png")]

    torch = [pygame.transform.scale(torch[0], (14, 20)), pygame.transform.scale(torch[1], (14, 20))]
    torch_counter = 0

    rogue = [pygame.image.load("assets/graphics/Rogue/Rogue.png"),
             pygame.image.load("assets/graphics/Rogue/Rogue_walk.png")]
    # rogue = [pygame.transform.flip(rogue[0], True, False), pygame.transform.flip(rogue[1], True, False)]
    background = pygame.image.load("assets/graphics/Level Elements/Floor/Floor.png")
    x, y = 20, 20
    quit_game = False

    while not quit_game:
        screen.fill(white)

        if torch_counter >= len(torch):
            torch_counter = 0

        screen.blit(background, (x, y))
        screen.blit(rogue[0], (x, y))

        screen.blit(torch[torch_counter], (200, 132))
        torch_counter += 1
        pygame.display.update()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                quit_game = True
                pygame.quit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:
                    print("press")
                    x, y = moveRight(screen, x, y, rogue, background, 8)


if __name__ == "__main__":
    main()
