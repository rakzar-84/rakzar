import json
import sys
import traceback

import pygame

import state
from core import draw_error
from loop import Loop
from screen import Screen

db = None
screen = None
try:
    with open("config.json", "r", encoding="utf-8") as file:
        state.config = json.load(file)
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
    sys.exit()
