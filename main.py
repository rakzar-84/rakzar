import json
import pygame
import sys
import traceback

from  errors import draw_error
import state
from screen import Screen
from loop import Loop

db = None
screen = None
try:
    with open('config.json', 'r', encoding='utf-8') as file:
        state.config = json.load(file)
    pygame.init()
    screen = Screen()
    screen.init()
    loop = Loop(screen)
    loop.init()
    loop.execute()
except Exception as e:
    print(traceback.format_exc())
    draw_error(screen.surface, e)
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