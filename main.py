import cProfile
import time

from entities.game import Game


# I think you're looking for run() in game.py
def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()

    # cProfile.run('main()', sort='cumtime')
