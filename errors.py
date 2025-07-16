import pygame
import traceback

import state


def draw_error(screen:pygame.surface.Surface, e:Exception):
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