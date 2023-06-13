import pygame


# def moveRight(screen, x, y, distance, speed):
#     guard = [pygame.image.load("assets/graphics/Ninja.png"),
#              pygame.image.load("assets/graphics/Ninja_walk.png")]
#     size = 32
#     guard = [pygame.transform.scale(guard[0], (size, size)), pygame.transform.scale(guard[1], (size, size))]
#     guard_right = [pygame.transform.scale(guard[0], (size, size)), pygame.transform.scale(guard[1], (size, size))]
#
#     guard_counter = 0
#     while True:
#         pygame.time.Clock().tick(speed)
#         screen.blit(guard_right[guard_counter], (x, y))
#         guard_counter += 1
#         x += 8




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

    guard = [pygame.image.load("assets/graphics/Rogue.png"),
             pygame.image.load("assets/graphics/Rogue_walk.png")]

    torch = [pygame.image.load("assets/graphics/Torch_small.png"),
             pygame.image.load("assets/graphics/Torch_big.png")]

    size = 32
    guard = [pygame.transform.scale(guard[0], (size, size)), pygame.transform.scale(guard[1], (size, size))]
    guard_right = [pygame.transform.scale(guard[0], (size, size)), pygame.transform.scale(guard[1], (size, size))]
    guard_left = [pygame.transform.flip(guard[0], True, False), pygame.transform.flip(guard[1], True, False)]
    torch = [pygame.transform.scale(torch[0], (14, 20)), pygame.transform.scale(torch[1], (14, 20))]

    clock = pygame.time.Clock()

    guard_counter = 0
    torch_counter = 0
    location = 100
    distance = 32*4
    move_right = True

    quit_game = False

    while not quit_game:
        clock.tick(4)
        screen.fill(white)

        if guard_counter >= len(guard):
            guard_counter = 0

        if torch_counter >= len(torch):
            torch_counter = 0

        if move_right:
            screen.blit(guard_right[guard_counter], (location, 100))
            guard_counter += 1
            location += 8

            if location - 100 >= distance:
                move_right = False
        else:
            screen.blit(guard_left[guard_counter], (location, 100))
            guard_counter += 1
            location -= 8

            if location <= 100:
                move_right = True

        screen.blit(torch[torch_counter], (200, 132))
        torch_counter += 1
        pygame.display.update()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                quit_game = True
                pygame.quit()


if __name__ == "__main__":
    main()
