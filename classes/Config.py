import os

# Base directory of the project (one level up from classes/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Virtual resolution for rendering
VIRTUAL_WIDTH = 640
VIRTUAL_HEIGHT = 480
TARGET_FPS = 60

# Platform flags (set before importing other game modules)
IS_MOBILE = False
DEBUG_MODE = True  # Enables mouse debug features (spawn enemies/coins)


def asset_path(relative_path):
    """Convert a relative path (e.g. './img/font.png') to an absolute path."""
    # Strip './' prefix if present
    if relative_path.startswith("./"):
        relative_path = relative_path[2:]
    return os.path.join(BASE_DIR, relative_path)
