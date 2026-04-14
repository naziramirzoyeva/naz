import pygame
import math
import time


class MickeysClock:
    """
    Draws a Mickey Mouse-style clock using rotating hand images.
    Right hand = minutes, Left hand = seconds.
    """

    def __init__(self, screen, center, hand_image_path):
        self.screen = screen
        self.center = center  # (x, y) center of the clock face

        # Load the hand image (used for both hands, just recolored/flipped if needed)
        try:
            original = pygame.image.load(hand_image_path).convert_alpha()
            # Scale hand to a reasonable size
            self.hand_image = pygame.transform.scale(original, (40, 120))
        except FileNotFoundError:
            # Fallback: draw a white rectangle as placeholder hand
            self.hand_image = self._create_placeholder_hand()

        self.font_large = pygame.font.SysFont("Arial", 72, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 28)

    def _create_placeholder_hand(self):
        """Creates a simple white hand shape if image is missing."""
        surf = pygame.Surface((20, 100), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        pygame.draw.rect(surf, (255, 255, 255), (5, 0, 10, 80))
        pygame.draw.circle(surf, (255, 255, 255), (10, 90), 10)
        return surf

    def _get_rotation_angle(self, value, max_value):
        """
        Convert time value to rotation angle.
        0 = pointing UP, angle increases clockwise.
        pygame.transform.rotate goes counter-clockwise, so we negate.
        """
        fraction = value / max_value          # 0.0 to <1.0
        degrees = fraction * 360              # 0 to 360
        return -degrees                       # negate for pygame (CW rotation)

    def _draw_hand(self, angle_deg):
        """Rotate hand image and blit it centered at self.center."""
        rotated = pygame.transform.rotate(self.hand_image, angle_deg)
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect)

    def draw(self):
        """Read system time and draw both clock hands + digital readout."""
        now = time.localtime()
        minutes = now.tm_min    # 0-59
        seconds = now.tm_sec    # 0-59

        # Calculate rotation angles
        min_angle = self._get_rotation_angle(minutes, 60)
        sec_angle = self._get_rotation_angle(seconds, 60)

        # Draw minute hand (right hand) — slightly larger / different tint
        min_hand = pygame.transform.scale(self.hand_image, (44, 130))
        rotated_min = pygame.transform.rotate(min_hand, min_angle)
        rect_min = rotated_min.get_rect(center=self.center)
        self.screen.blit(rotated_min, rect_min)

        # Draw second hand (left hand) — slightly smaller
        sec_hand = pygame.transform.scale(self.hand_image, (32, 110))
        rotated_sec = pygame.transform.rotate(sec_hand, sec_angle)
        rect_sec = rotated_sec.get_rect(center=self.center)
        self.screen.blit(rotated_sec, rect_sec)

        # Draw center dot
        pygame.draw.circle(self.screen, (255, 0, 0), self.center, 8)

        # Draw digital time below clock
        time_str = time.strftime("%M:%S", now)
        text_surf = self.font_large.render(time_str, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.center[0], self.center[1] + 200))
        self.screen.blit(text_surf, text_rect)

        # Draw labels
        label_min = self.font_small.render("Right Hand = Minutes", True, (200, 200, 200))
        label_sec = self.font_small.render("Left Hand  = Seconds", True, (200, 200, 200))
        self.screen.blit(label_min, label_min.get_rect(center=(self.center[0], self.center[1] + 260)))
        self.screen.blit(label_sec, label_sec.get_rect(center=(self.center[0], self.center[1] + 295)))