import pygame

from classes.Config import VIRTUAL_WIDTH, VIRTUAL_HEIGHT


class TouchController:
    """Draws a semi-transparent touch UI overlay and maps touch/mouse events
    to game input states. Works with both desktop mouse and Android touch."""

    def __init__(self):
        # Virtual button states
        self.btn_left = False
        self.btn_right = False
        self.btn_jump = False
        self.btn_boost = False
        self.btn_pause = False

        # Menu/click tracking
        self.touch_down = False
        self.touch_up = False
        self.touch_point = None  # (x, y) in virtual coords for click detection
        self._was_touch = False  # track edge for single-click detection

        # Active touch/mouse finger IDs
        self._active_touches = {}  # finger_id -> (vx, vy)

    # ---- Button hit areas in virtual 640x480 space ----

    # D-pad zone: bottom-left
    D_PAD_ZONE = pygame.Rect(10, 330, 200, 140)
    # Within the D-pad zone, split left/right at the midpoint
    D_PAD_SPLIT_X = 110  # absolute virtual x coordinate of the split

    # Jump button: large circle, bottom-right
    JUMP_CENTER = (560, 400)
    JUMP_RADIUS = 45

    # Boost/run button: smaller circle, above and left of jump
    BOOST_CENTER = (490, 380)
    BOOST_RADIUS = 25

    # Pause button: top-right corner
    PAUSE_ZONE = pygame.Rect(590, 10, 40, 30)

    def screen_to_virtual(self, sx, sy, screen_w, screen_h):
        """Convert actual screen coordinates to 640x480 virtual coordinates.
        Assumes the game is rendered centered with letterboxing."""
        scale = min(screen_w / VIRTUAL_WIDTH, screen_h / VIRTUAL_HEIGHT)
        offset_x = (screen_w - VIRTUAL_WIDTH * scale) / 2
        offset_y = (screen_h - VIRTUAL_HEIGHT * scale) / 2
        vx = (sx - offset_x) / scale
        vy = (sy - offset_y) / scale
        return vx, vy

    def _hit_test(self, vx, vy):
        """Determine which button (if any) the virtual point (vx, vy) hits."""
        # Pause button
        if self.PAUSE_ZONE.collidepoint(vx, vy):
            return "pause"

        # D-pad zone
        if self.D_PAD_ZONE.collidepoint(vx, vy):
            if vx < self.D_PAD_SPLIT_X:
                return "left"
            else:
                return "right"

        # Boost button (checked before jump because it's smaller and may overlap)
        bx, by = self.BOOST_CENTER
        if (vx - bx) ** 2 + (vy - by) ** 2 <= self.BOOST_RADIUS ** 2:
            return "boost"

        # Jump button
        jx, jy = self.JUMP_CENTER
        if (vx - jx) ** 2 + (vy - jy) ** 2 <= self.JUMP_RADIUS ** 2:
            return "jump"

        return None

    def process_events(self, events, screen_w=None, screen_h=None):
        """Process pygame events (MOUSEBUTTONDOWN/UP, FINGERDOWN/UP/MOTION).
        If screen_w/screen_h not given, assumes 1:1 virtual-to-screen mapping."""
        if screen_w is None:
            screen_w = VIRTUAL_WIDTH
        if screen_h is None:
            screen_h = VIRTUAL_HEIGHT

        # Reset edge-triggered flags
        self.touch_down = False
        self.touch_up = False
        self._was_touch = self.touch_point is not None

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                vx, vy = self.screen_to_virtual(event.pos[0], event.pos[1], screen_w, screen_h)
                self._on_down(vx, vy, 0)
                self.touch_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                vx, vy = self.screen_to_virtual(event.pos[0], event.pos[1], screen_w, screen_h)
                self._on_up(vx, vy, 0)
                self.touch_up = True
            elif event.type == pygame.FINGERDOWN:
                vx = event.x * screen_w
                vy = event.y * screen_h
                vx, vy = self.screen_to_virtual(vx, vy, screen_w, screen_h)
                self._on_down(vx, vy, event.finger_id)
                self.touch_down = True
            elif event.type == pygame.FINGERUP:
                vx = event.x * screen_w
                vy = event.y * screen_h
                vx, vy = self.screen_to_virtual(vx, vy, screen_w, screen_h)
                self._on_up(vx, vy, event.finger_id)
                self.touch_up = True
            elif event.type == pygame.FINGERMOTION:
                vx = event.x * screen_w
                vy = event.y * screen_h
                vx, vy = self.screen_to_virtual(vx, vy, screen_w, screen_h)
                self._on_move(vx, vy, event.finger_id)

    def _on_down(self, vx, vy, finger_id):
        hit = self._hit_test(vx, vy)
        self._active_touches[finger_id] = (vx, vy, hit)
        if hit == "left":
            self.btn_left = True
        elif hit == "right":
            self.btn_right = True
        elif hit == "jump":
            self.btn_jump = True
        elif hit == "boost":
            self.btn_boost = True
        elif hit == "pause":
            self.btn_pause = True
        # Always record the touch point for menu clicks
        self.touch_point = (vx, vy)

    def _on_up(self, vx, vy, finger_id):
        if finger_id in self._active_touches:
            _, _, prev_hit = self._active_touches.pop(finger_id)
            if prev_hit == "left":
                self.btn_left = False
            elif prev_hit == "right":
                self.btn_right = False
            elif prev_hit == "jump":
                self.btn_jump = False
            elif prev_hit == "boost":
                self.btn_boost = False
        # Keep touch_point for one frame after release for menu click detection
        self.touch_point = (vx, vy)

    def _on_move(self, vx, vy, finger_id):
        if finger_id in self._active_touches:
            prev_vx, prev_vy, prev_hit = self._active_touches[finger_id]
            hit = self._hit_test(vx, vy)
            if hit != prev_hit:
                # Left the previous hit zone
                if prev_hit == "left":
                    self.btn_left = False
                elif prev_hit == "right":
                    self.btn_right = False
                elif prev_hit == "jump":
                    self.btn_jump = False
                elif prev_hit == "boost":
                    self.btn_boost = False
                # Entered new hit zone
                if hit == "left":
                    self.btn_left = True
                elif hit == "right":
                    self.btn_right = True
                elif hit == "jump":
                    self.btn_jump = True
                elif hit == "boost":
                    self.btn_boost = True
                self._active_touches[finger_id] = (vx, vy, hit)

    def fill_input_state(self, state):
        """Fill an InputState object from current button states."""
        state.left = self.btn_left
        state.right = self.btn_right
        state.jump = self.btn_jump
        state.boost = self.btn_boost
        state.pause = self.btn_pause

    def consume_click(self):
        """Return the current touch_point and clear it (for menu single-click)."""
        pt = self.touch_point
        self.touch_point = None
        return pt

    def draw(self, surface):
        """Draw semi-transparent touch controls onto the given surface.
        Surface should be in virtual 640x480 coordinates."""

        # Create a transparent overlay
        overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)

        # D-pad background
        dpad_color = (255, 255, 255, 40)
        left_color = (255, 255, 255, 80) if self.btn_left else (255, 255, 255, 25)
        right_color = (255, 255, 255, 80) if self.btn_right else (255, 255, 255, 25)

        # Draw D-pad base
        pygame.draw.rect(overlay, dpad_color, self.D_PAD_ZONE, border_radius=12)

        # Left half
        left_rect = pygame.Rect(
            self.D_PAD_ZONE.x, self.D_PAD_ZONE.y,
            self.D_PAD_SPLIT_X - self.D_PAD_ZONE.x, self.D_PAD_ZONE.height
        )
        pygame.draw.rect(overlay, left_color, left_rect, border_radius=10)

        # Right half
        right_rect = pygame.Rect(
            self.D_PAD_SPLIT_X, self.D_PAD_ZONE.y,
            self.D_PAD_ZONE.right - self.D_PAD_SPLIT_X, self.D_PAD_ZONE.height
        )
        pygame.draw.rect(overlay, right_color, right_rect, border_radius=10)

        # Direction arrows
        arrow_color = (255, 255, 255, 120)
        # Left arrow
        cx, cy = 60, 400
        points_left = [(cx + 15, cy - 15), (cx - 10, cy), (cx + 15, cy + 15)]
        pygame.draw.polygon(overlay, arrow_color, points_left)
        # Right arrow
        cx, cy = 155, 400
        points_right = [(cx - 15, cy - 15), (cx + 10, cy), (cx - 15, cy + 15)]
        pygame.draw.polygon(overlay, arrow_color, points_right)

        # Jump button
        jump_color = (100, 200, 100, 80) if self.btn_jump else (100, 200, 100, 40)
        pygame.draw.circle(overlay, jump_color, self.JUMP_CENTER, self.JUMP_RADIUS)
        # Jump label
        font = pygame.font.Font(None, 20)
        jump_text = font.render("JUMP", True, (255, 255, 255, 100))
        overlay.blit(jump_text, (self.JUMP_CENTER[0] - 18, self.JUMP_CENTER[1] - 6))

        # Boost button
        boost_color = (200, 150, 50, 80) if self.btn_boost else (200, 150, 50, 40)
        pygame.draw.circle(overlay, boost_color, self.BOOST_CENTER, self.BOOST_RADIUS)
        boost_text = font.render("RUN", True, (255, 255, 255, 100))
        overlay.blit(boost_text, (self.BOOST_CENTER[0] - 14, self.BOOST_CENTER[1] - 6))

        # Pause button
        pause_color = (200, 200, 200, 80) if self.btn_pause else (200, 200, 200, 40)
        pygame.draw.rect(overlay, pause_color, self.PAUSE_ZONE, border_radius=4)
        # Pause icon (two vertical bars)
        bar_color = (255, 255, 255, 120)
        pygame.draw.rect(overlay, bar_color, (self.PAUSE_ZONE.x + 8, self.PAUSE_ZONE.y + 6, 5, 18))
        pygame.draw.rect(overlay, bar_color, (self.PAUSE_ZONE.x + 20, self.PAUSE_ZONE.y + 6, 5, 18))

        surface.blit(overlay, (0, 0))
