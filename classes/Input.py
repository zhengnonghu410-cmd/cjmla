import pygame
from pygame.locals import *
import sys

from classes.Config import DEBUG_MODE
from classes.InputState import InputState


class InputProvider:
    """Abstract base for input providers. Subclasses implement poll()."""

    def poll(self, events):
        """Return an InputState for the current frame."""
        raise NotImplementedError


class KeyboardProvider(InputProvider):
    """Reads keyboard and mouse, returns InputState. Matches original behavior."""

    def __init__(self, entity=None):
        self.entity = entity  # Mario instance (for gameplay mouse debug features)

    def poll(self, events):
        state = InputState()

        # Check quit and restart events
        for event in events:
            if event.type == pygame.QUIT:
                state.quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F5:
                    state.pause = True

                # Menu-style navigation keys (also used in-game for jump direction)
                if event.key == pygame.K_UP or event.key == pygame.K_k:
                    state.up = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_j:
                    state.down = True
                if event.key == pygame.K_RETURN:
                    state.confirm = True
                if event.key == pygame.K_ESCAPE:
                    state.back = True

        # Keyboard held state
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[K_LEFT] or pressedKeys[K_h] and not pressedKeys[K_RIGHT]:
            state.left = True
        elif pressedKeys[K_RIGHT] or pressedKeys[K_l] and not pressedKeys[K_LEFT]:
            state.right = True

        state.jump = pressedKeys[K_SPACE] or pressedKeys[K_UP] or pressedKeys[K_k]
        state.boost = pressedKeys[K_LSHIFT]

        # Debug mouse features (spawn enemies/coins) - only on desktop
        if DEBUG_MODE and self.entity is not None:
            for e in events:
                if e.type == pygame.MOUSEBUTTONUP:
                    mx, my = pygame.mouse.get_pos()
                    if e.button == 1:  # Left click: spawn coin
                        self.entity.levelObj.addCoin(
                            mx / 32 - self.entity.camera.pos.x, my / 32
                        )
                    elif e.button == 3:  # Right click: spawn enemies
                        self.entity.levelObj.addKoopa(
                            my / 32, mx / 32 - self.entity.camera.pos.x
                        )
                        self.entity.levelObj.addGoomba(
                            my / 32, mx / 32 - self.entity.camera.pos.x
                        )
                        self.entity.levelObj.addRedMushroom(
                            my / 32, mx / 32 - self.entity.camera.pos.x
                        )

        return state


class TouchProvider(InputProvider):
    """Touch input provider — stub for now, will be fleshed out in Phase 3."""

    def __init__(self, touch_controller=None):
        self.touch_controller = touch_controller

    def poll(self, events):
        state = InputState()
        # Process touch/mouse events through the touch controller
        if self.touch_controller:
            self.touch_controller.process_events(events)
            self.touch_controller.fill_input_state(state)
        # Also handle quit
        for event in events:
            if event.type == pygame.QUIT:
                state.quit = True
        return state


# ---- Legacy Input class for Mario entity compatibility during transition ----
class Input:
    """Thin wrapper used by Mario. Delegates to a KeyboardProvider internally.
    This preserves the original API while the provider is established."""

    def __init__(self, entity):
        self.entity = entity
        self._provider = KeyboardProvider(entity)

    def checkForInput(self):
        events = pygame.event.get()
        state = self._provider.poll(events)

        # Apply input state to entity traits (same logic as original)
        if state.left:
            self.entity.traits["goTrait"].direction = -1
        elif state.right:
            self.entity.traits["goTrait"].direction = 1
        else:
            self.entity.traits['goTrait'].direction = 0

        self.entity.traits['jumpTrait'].jump(state.jump)
        self.entity.traits['goTrait'].boost = state.boost

        if state.pause and not self.entity.pause:
            self.entity.pause = True
            self.entity.pauseObj.createBackgroundBlur()

        if state.quit:
            pygame.quit()
            sys.exit()
