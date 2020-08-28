import time
import threading

from .logger import Logger
from .interpreter import interpret


class TimedStringBuffer:
    """Buffers the keypresses to be logged, flushing only after a certain time 
    threshold is exceeded.
    """
    STEP_TIME_SECONDS = 0.5

    def __init__(self, logger, threshold=1.0, render_backspaces=False):
        self.threshold = threshold
        self.render_backspaces = render_backspaces

        self.flush_counter = 0

        self.last_keypress = time.time()
        self.logger = logger

        self.flush()
        self.start()
    
    def __str__(self):
        return self.string
    
    def add(self, event):
        self.flush_counter = self.threshold

        if event.name == 'backspace' and self.render_backspaces:
            self.events.pop()
        else:
            self.events.append(event)
    
    def flush(self):
        self.events = []
    
    def start(self):
        
        def listener():
            while True:

                if self.flush_counter <= 0:
                    if self.events:
                        self.flush_counter = 0

                        string = interpret(self.events)                        
                        if string: self.logger.keypress(string)
                        self.flush()

                else:
                    self.flush_counter -= self.STEP_TIME_SECONDS

                time.sleep(self.STEP_TIME_SECONDS)
        
        self.listener = threading.Thread(target=listener, daemon = True)
        self.listener.start()

        return self
    