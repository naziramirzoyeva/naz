"""
Music Player with Keyboard Controller
======================================

Controls:
P  - Play
S  - Stop
SPACE - Pause/Resume
N  - Next track
B  - Previous track
Q  - Quit
"""

import pygame
import sys
from player import MusicPlayer


# ── Settings ─────────────────────────────
WIDTH, HEIGHT = 640, 480
FPS = 30

# Colors
BG = (18, 18, 28)
PANEL = (30, 30, 50)
ACCENT = (0, 200, 120)
WHITE = (240, 240, 240)
GRAY = (150, 150, 170)
DARK = (80, 80, 100)
YELLOW = (255, 220, 0)
RED = (220, 60, 60)


def draw_bar(screen, x, y, w, h, value):
    pygame.draw.rect(screen, DARK, (x, y, w, h), border_radius=6)
    fill = min(value % 60, 60) / 60 * w
    pygame.draw.rect(screen, ACCENT, (x, y, fill, h), border_radius=6)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("Arial", 40, bold=True)
    font = pygame.font.SysFont("Arial", 22)
    font_small = pygame.font.SysFont("Arial", 18)

    player = MusicPlayer("music_player/music")

    running = True

    while running:
        # ── Events ─────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_SPACE:
                    player.pause_resume()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()

        player.update()

        # ── Draw ───────────────────────────
        screen.fill(BG)

        # Title
        title = font_title.render("Music Player", True, ACCENT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

        # Panel
        pygame.draw.rect(screen, PANEL, (40, 100, 560, 140), border_radius=12)

        if player.get_total_tracks() > 0:
            name = player.get_track_name()
            name_text = font.render(name, True, WHITE)
            screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, 130))

            counter = f"{player.current_index+1} / {player.get_total_tracks()}"
            counter_text = font_small.render(counter, True, GRAY)
            screen.blit(counter_text, (WIDTH//2 - counter_text.get_width()//2, 160))

            pos = player.get_position_seconds()
            draw_bar(screen, 80, 190, 480, 12, pos)

            time_text = font_small.render(f"{pos}s", True, GRAY)
            screen.blit(time_text, (80, 210))

        else:
            error = font.render("No music in folder", True, RED)
            screen.blit(error, (WIDTH//2 - error.get_width()//2, 150))

        # Status
        status = font.render(player.get_status(), True, YELLOW)
        screen.blit(status, (WIDTH//2 - status.get_width()//2, 270))

        # Controls
        controls = [
            "P - Play",
            "S - Stop",
            "SPACE - Pause",
            "N - Next",
            "B - Back",
            "Q - Quit"
        ]

        y = 320
        for c in controls:
            text = font_small.render(c, True, GRAY)
            screen.blit(text, (60, y))
            y += 25

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()