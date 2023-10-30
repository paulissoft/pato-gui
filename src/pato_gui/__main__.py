import sys

from pato_gui.app import main


if __name__ == '__main__':
    sys.argv[0] = 'environment'  # A nicer name for the the first screen than __main__
    main()
