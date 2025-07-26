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
        if state.config["debug"]:
            self.deltas.append({"start": time.perf_counter()})

    def take(self, label: str):
        if state.config["debug"]:
            if self.deltas:
                self.deltas[-1][label] = time.perf_counter()

    def print(self):
        if state.config["debug"]:
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
        if state.config["debug"]:
            for step in self.deltas[-5:]:
                delta = step[label_to] - step[label_from]
                print(f"{label} time: {delta*1000:.2f} ms")


def draw_error(e: Exception):
    screen_info = pygame.display.Info()
    w = screen_info.current_w - 100
    h = screen_info.current_h - 100
    screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    y = 10
    font = pygame.font.SysFont(None, 24)
    if state.config["debug"]:
        error_text = traceback.format_exc()
    else:
        error_text = str(e)
    for line in error_text.splitlines():
        text_surface = font.render(line, True, (255, 0, 0))
        screen.blit(text_surface, (10, y))
        y += 30
    pygame.display.flip()
