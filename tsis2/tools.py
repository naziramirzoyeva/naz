import pygame
from collections import deque
from datetime import datetime

WHITE = (255, 255, 255)

class Tools:

    def flood_fill(self, surface, start, target_color, fill_color, w, h):
        if target_color == fill_color:
            return

        q = deque([start])

        while q:
            x, y = q.popleft()

            if x < 0 or y < 0 or x >= w or y >= h:
                continue

            if surface.get_at((x, y)) != target_color:
                continue

            surface.set_at((x, y), fill_color)

            q.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])

    def save(self, surface):
        name = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
        pygame.image.save(surface, name)
        print("saved:", name)