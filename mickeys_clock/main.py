"""
Mickey's Clock Application
==========================
Displays current minutes and seconds using Mickey Mouse hand graphics.
Right hand = minutes hand | Left hand = seconds hand
Updates every second in real-time.
"""

import pygame
import sys
import os
from clock import MickeysClock

# ── Constants ────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 700
FPS           = 1          # 1 frame per second — clock only needs 1 Hz
BG_COLOR      = (30, 30, 60)   # Dark blue background

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HAND_IMAGE_PATH = os.path.join(BASE_DIR, "images", "mickey_hand.png")


def draw_clock_face(screen, center, radius=180):
    """Draw a decorative clock face circle with hour markers."""
    # Outer ring
    pygame.draw.circle(screen, (255, 220, 0), center, radius, 6)
    # Inner fill
    pygame.draw.circle(screen, (50, 50, 90), center, radius - 6)

    # Draw 12 tick marks
    import math
    for i in range(60):
        angle_rad = math.radians(i * 6 - 90)   # start from top
        if i % 5 == 0:
            # Hour marker — longer tick
            inner = radius - 24
            outer = radius - 8
            color = (255, 220, 0)
            width = 3
        else:
            # Minute marker — short tick
            inner = radius - 14
            outer = radius - 8
            color = (180, 180, 180)
            width = 1
        x1 = center[0] + inner * math.cos(angle_rad)
        y1 = center[1] + inner * math.sin(angle_rad)
        x2 = center[0] + outer * math.cos(angle_rad)
        y2 = center[1] + outer * math.sin(angle_rad)
        pygame.draw.line(screen, color, (int(x1), int(y1)), (int(x2), int(y2)), width)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mickey's Clock ")
    clock_tick = pygame.time.Clock()

    # Center of the clock face
    center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)

    # Instantiate clock object
    mickey_clock = MickeysClock(screen, center, HAND_IMAGE_PATH)

    # Title font
    title_font = pygame.font.SysFont("Arial", 36, bold=True)

    running = True
    while running:
        # ── Event handling ───────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        # ── Drawing ──────────────────────────────────────────────────────
        screen.fill(BG_COLOR)

        # Title
        title = title_font.render("Mickey's Clock", True, (255, 220, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 40)))

        # Clock face decoration
        draw_clock_face(screen, center)

        # Clock hands + digital display
        mickey_clock.draw()

        # Quit hint
        hint_font = pygame.font.SysFont("Arial", 20)
        hint = hint_font.render("Press Q to quit", True, (150, 150, 150))
        screen.blit(hint, (10, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        clock_tick.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()