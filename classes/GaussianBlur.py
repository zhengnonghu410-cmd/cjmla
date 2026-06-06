import pygame


class GaussianBlur:
    def __init__(self, kernelsize=7):
        self.kernel_size = kernelsize

    def filter(self, srfc, xpos, ypos, width, height):
        # Use pygame's smoothscale down-then-up as a cheap blur approximation.
        # This avoids scipy/numpy dependencies which are problematic on Android.
        sub = srfc.subsurface((xpos, ypos, width, height))
        small = pygame.transform.smoothscale(sub, (width // 8, height // 8))
        blurred = pygame.transform.smoothscale(small, (width, height))
        return blurred
