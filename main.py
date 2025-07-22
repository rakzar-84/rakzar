import json
import sys
import traceback

import pygame

import state
from cache import Cache
from core import Profiler, draw_error
from loop import Loop
from screen import Screen

db = None
screen = None
try:
    with open("config.json", encoding="utf-8") as file:
        state.config = json.load(file)
    state.cache = Cache()
    state.profiler = Profiler()
    pygame.init()
    screen = Screen()
    screen.init()
    loop = Loop(screen)
    loop.init()
    loop.execute()
except Exception as e:
    print(traceback.format_exc())
    draw_error(screen.image, e)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
finally:
    if db:
        db.close()
    pygame.quit()
    state.profiler.print()
    # debug
    # state.profiler.print_specific("tot", "start", "end")
    sys.exit()
