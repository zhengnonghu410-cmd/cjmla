import pygame
from classes.Config import asset_path, VIRTUAL_WIDTH, VIRTUAL_HEIGHT, TARGET_FPS, IS_MOBILE, DEBUG_MODE
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from classes.TouchController import TouchController
from entities.Mario import Mario


def get_screen_size():
    """Determine the actual screen/window size."""
    if IS_MOBILE:
        # On Android, use fullscreen native resolution
        return None  # set_mode((0, 0), FULLSCREEN) handles this
    else:
        # Desktop: use virtual resolution by default (can be resized)
        return (VIRTUAL_WIDTH, VIRTUAL_HEIGHT)


def compute_scale_and_offset(actual_w, actual_h):
    """Compute scale factor and offset to center the game with letterboxing."""
    scale = min(actual_w / VIRTUAL_WIDTH, actual_h / VIRTUAL_HEIGHT)
    offset_x = (actual_w - VIRTUAL_WIDTH * scale) / 2
    offset_y = (actual_h - VIRTUAL_HEIGHT * scale) / 2
    return scale, offset_x, offset_y


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    # Set up display
    if IS_MOBILE:
        actual_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        actual_w, actual_h = actual_screen.get_size()
    else:
        actual_screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        actual_w, actual_h = VIRTUAL_WIDTH, VIRTUAL_HEIGHT

    # Virtual surface where all game rendering happens at 640x480
    virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

    # Touch controller (always created; only shown/used on mobile or when DEBUG_MODE on)
    touch_controller = TouchController()

    # Create game objects — they render to virtual_screen
    dashboard = Dashboard(asset_path("./img/font.png"), 8, virtual_screen)
    sound = Sound()
    level = Level(virtual_screen, sound, dashboard)
    menu = Menu(virtual_screen, dashboard, level, sound)

    # Menu loop
    while not menu.start:
        menu.checkInput()  # Menu handles its own event loop + display update
        # Scale and present the virtual screen
        scale, ox, oy = compute_scale_and_offset(actual_w, actual_h)
        scaled = pygame.transform.scale(virtual_screen, (
            int(VIRTUAL_WIDTH * scale), int(VIRTUAL_HEIGHT * scale)
        ))
        actual_screen.fill((0, 0, 0))
        actual_screen.blit(scaled, (ox, oy))

        # Draw touch controls on the actual screen (not virtual, so they stay crisp)
        if IS_MOBILE or DEBUG_MODE:
            touch_controller.draw(actual_screen)

        pygame.display.update()

    mario = Mario(0, 0, level, virtual_screen, dashboard, sound)
    clock = pygame.time.Clock()

    # Gameplay loop
    while not mario.restart:
        # Pump events once per frame
        events = pygame.event.get()

        # Let touch controller process events
        scale, ox, oy = compute_scale_and_offset(actual_w, actual_h)
        touch_controller.process_events(events, actual_w, actual_h)

        # Check for quit through events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'quit'

        pygame.display.set_caption(
            "Super Mario running with {:d} FPS".format(int(clock.get_fps()))
        )

        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()

        # Scale virtual screen to actual screen
        scaled = pygame.transform.scale(virtual_screen, (
            int(VIRTUAL_WIDTH * scale), int(VIRTUAL_HEIGHT * scale)
        ))
        actual_screen.fill((0, 0, 0))
        actual_screen.blit(scaled, (ox, oy))

        # Draw touch controls overlay
        if IS_MOBILE or DEBUG_MODE:
            touch_controller.draw(actual_screen)

        pygame.display.update()
        clock.tick(TARGET_FPS)

    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
