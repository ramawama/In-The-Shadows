import sys
sys.path.insert(1, './entities/')
from game import Game

# I think you're looking for run() in game.py
def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()