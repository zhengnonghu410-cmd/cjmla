class InputState:
    """Holds the current frame's input state as simple booleans/values.
    This decouples game logic from the physical input source (keyboard vs touch).
    """

    def __init__(self):
        # Gameplay actions
        self.left = False
        self.right = False
        self.jump = False
        self.boost = False
        self.pause = False

        # Menu navigation
        self.up = False
        self.down = False
        self.confirm = False
        self.back = False

        # Touch/mouse click point in screen coordinates (None if no click)
        self.touch_point = None

        # Quit signal
        self.quit = False
