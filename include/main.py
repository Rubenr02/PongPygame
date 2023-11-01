import sys, src.interface
from src.config import *


def main():
    """ Main function """
    if len(sys.argv) == 4:  # if received resolution, sound on/off as arguments
        settings = GlobalSettings((int(sys.argv[1]), int(sys.argv[2])), bool(sys.argv[3]))

    else:  # if not, use default resolution and sound on
        settings = GlobalSettings()

    # Initialize Interface with settings
    thePongVerseGame = src.interface.Interface(settings)
    thePongVerseGame.mainMenu()


if __name__ == '__main__':
    main()
