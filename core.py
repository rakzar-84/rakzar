import time
import traceback

import pygame

import state


class GSprite(pygame.sprite.Sprite):

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, *groups: pygame.sprite.Group):
        super().__init__(groups)
        self.image = None
        self.rect = None


class Profiler:

    start: float
    deltas: list

    def __init__(self):
        self.deltas = []

    def reset(self):
        self.deltas.append({"start": time.perf_counter()})

    def take(self, label: str):
        if self.deltas:
            self.deltas[-1][label] = time.perf_counter()

    def print(self):
        last = 0
        for step in self.deltas[-5:]:
            for label in step:
                if last:
                    delta = step[label] - last
                    print(f"{label} time: {delta*1000:.2f} ms")
                else:
                    print(f"{label}")
                last = step[label]

    def print_specific(self, label: int, label_from: str, label_to: str):
        for step in self.deltas[-5:]:
            delta = step[label_to] - step[label_from]
            print(f"{label} time: {delta*1000:.2f} ms")


def draw_error(screen: pygame.surface.Surface, e: Exception):
    if screen:
        screen.fill((0, 0, 0))
        y = 10
        font = pygame.font.SysFont(None, 24)
        if "debug" in state.config and state.config["debug"]:
            error_text = traceback.format_exc()
        else:
            error_text = str(e)
        for line in error_text.splitlines():
            text_surface = font.render(line, True, (255, 0, 0))
            screen.blit(text_surface, (10, y))
            y += 30
        pygame.display.flip()
