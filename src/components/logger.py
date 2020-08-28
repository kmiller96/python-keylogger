import sys
import logging

from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler

KEYPRESS_LOG_HEIGHT = 100  # In library CRITICAL = 50, DEBUG=10


def Logger(fpath, rotation_interval, rotation_frequency):
    """Monkey-patched logging object.
    
    There is no point creating a new class when we only need to extend the base
    logger. We monkey-patch rather than inherit & overwrite to avoid unintended
    consequences as well as to put the "script" logic along the "monkey-patching" 
    logic (e.g. logging.addLevelName).
    """

    def keypress_func(msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(KEYPRESS_LOG_HEIGHT):
            logging.log(KEYPRESS_LOG_HEIGHT, msg)

    logging.addLevelName(KEYPRESS_LOG_HEIGHT, 'KEYPRESS')  
    logging.keypress = keypress_func

    logging.basicConfig(
        level = KEYPRESS_LOG_HEIGHT,
        format = '[%(asctime)s] %(message)s',
        handlers = [
            StreamHandler(stream=sys.stdout),
            TimedRotatingFileHandler(
                filename=fpath,
                when=rotation_interval,
                interval=rotation_frequency,
            )
        ]
    )

    logger = logging.getLogger("KEYLOGGER")
    logger.keypress = keypress_func
    return logger
