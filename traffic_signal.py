import pygame
from config import *


class TrafficSignal:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.state = "RED"
        self.timer = DEFAULT_GREEN

        self.radius = 12

    # =====================================
    # Change Signal
    # =====================================

    def set_state(self, state):

        self.state = state

    # =====================================
    # Check State
    # =====================================

    def is_red(self):

        return self.state == "RED"

    def is_yellow(self):

        return self.state == "YELLOW"

    def is_green(self):

        return self.state == "GREEN"

    # =====================================
    # Draw Glow
    # =====================================

    def draw_glow(self, screen, color):

        for i in range(20, 0, -4):

            surface = pygame.Surface(
                (i * 4, i * 4),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                surface,
                (*color, 20),
                (i * 2, i * 2),
                i
            )

            screen.blit(
                surface,
                (
                    self.x - i * 2,
                    self.y - i * 2
                )
            )

    # =====================================
    # Draw
    # =====================================

    def draw(self, screen):

        # Pole

        pygame.draw.rect(
            screen,
            DARK_GRAY,
            (
                self.x - 6,
                self.y,
                12,
                80
            )
        )

        # Box

        box = pygame.Rect(
            self.x - 20,
            self.y - 55,
            40,
            90
        )

        pygame.draw.rect(
            screen,
            BLACK,
            box,
            border_radius=8
        )

        red = DARK_GRAY
        yellow = DARK_GRAY
        green = DARK_GRAY

        if self.is_red():

            red = RED
            self.draw_glow(screen, RED)

        elif self.is_yellow():

            yellow = YELLOW
            self.draw_glow(screen, YELLOW)

        elif self.is_green():

            green = GREEN
            self.draw_glow(screen, GREEN)

        pygame.draw.circle(
            screen,
            red,
            (self.x, self.y - 35),
            self.radius
        )

        pygame.draw.circle(
            screen,
            yellow,
            (self.x, self.y - 10),
            self.radius
        )

        pygame.draw.circle(
            screen,
            green,
            (self.x, self.y + 15),
            self.radius
        )

        # Countdown

        text = FONT_SMALL.render(
            str(self.timer),
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                self.x - 8,
                self.y + 45
            )
        )