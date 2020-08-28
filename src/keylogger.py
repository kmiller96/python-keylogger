import configparser
import os
import shutil
import sys

import keyboard

from components.logger import Logger
from components.buffer import TimedStringBuffer

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['default']

    make_logging_directory_if_not_exists(directory=config.get('logging_path'))

    logger = Logger(
        fpath=os.path.join(config.get('logging_path'), 'log'),
        rotation_interval=config.get('log_rotation_interval'),
        rotation_frequency=config.getint('log_rotation_frequency'),
    )

    buffer = TimedStringBuffer(
        logger = logger, 
        threshold = config.getfloat('sentence_max_delta_seconds'),
        render_backspaces = config.getboolean('render_backspaces')
    )
    keyboard.on_press(callback=buffer.add)

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        sys.exit(0)
    

def make_logging_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    main()