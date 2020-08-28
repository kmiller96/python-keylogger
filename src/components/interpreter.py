import keyboard

DISALLOWED_CHARS = {  # NOTE: Currently unused.
    'shift',
    'ctrl'
}

CHAR_RENAME_MAP = {
    'enter': {
        'multi': ' [ENTER] ',
        'single': '[ENTER]',
    },

    'space': {
        'multi': ' ',
        'single': '[SPACE]'
    },
    
    'tab': '[TAB]',
    'backspace': '[BACKSPACE]',
    'right': '[RIGHT]',
    'left': '[LEFT]',
}


def interpret(events):
    """Interprets the key press events and formats them into the desired format."""
    string = ''
    sequence_buffer = []
    style = 'multi' if len(events) > 1 else 'single'

    for e in events:
        char = e.name

        if char in DISALLOWED_CHARS:
            continue
        
        try:
            char = CHAR_RENAME_MAP[char]
            if isinstance(char, dict):
                char = char[style]
        except KeyError:
            char = char  # Redundant, but done for readability
        
        if keyboard.is_pressed('ctrl'):
            string += f"[CTRL+{char}]"
        elif keyboard.is_pressed('shift'):
            string += f"[SHIFT+{char}]"
        else:
            string += char

    return string 
