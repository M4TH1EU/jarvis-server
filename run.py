import os
import sys

# TODO: see if something better could be done
if __name__ == '__main__':
    sys.path.append(os.path.realpath('..'))

    # doing the import after editing the path otherwise cause issue between running in pycharm or the terminal
    from jarvis.main import start

    start()
