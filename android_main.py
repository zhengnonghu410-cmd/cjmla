"""
Android entry point for the Super Mario game.
This sets platform flags before importing the main game module.
"""

# Must be set BEFORE importing any game modules
import classes.Config as Config
Config.IS_MOBILE = True
Config.DEBUG_MODE = False

# Now import and run the game
from main import main

if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
