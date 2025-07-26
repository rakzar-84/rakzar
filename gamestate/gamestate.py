from typing import TYPE_CHECKING

import pygame

import state
from gamestate.interface.interface import Interface

if TYPE_CHECKING:
    from db import Db


class GameState:

    STATE_CODE = ""

    interface: Interface

    def __init__(self):
        self.interface = Interface()

    def init(self, db: "Db"):
        self.interface.init()
        pass

    def check_input(self):
        state.keys = pygame.key.get_pressed()
        state.mouse = {}
        for event in pygame.event.get():
            # todo quali altri eventi?
            # MOUSEWHEEL
            # USEREVENT
            # TEXTINPUT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.interface.to_window()
                    state.resize = True
                elif event.key == pygame.K_F12:
                    self.interface.to_fullscreen()
                    state.resize = True
            if event.type == pygame.VIDEORESIZE:
                state.resize = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                state.mouse["pos"] = event.pos
                if event.button == 1:
                    state.mouse["button"] = "left"
                elif event.button == 3:
                    state.mouse["button"] = "right"
                else:
                    state.mouse["button"] = ""
            if event.type == pygame.QUIT:
                state.running = GameState.STATE_CODE

    def update(self):
        self.interface.update()

    def do_interaction(self):
        pass

    def animate(self):
        pass

    def audio(self):
        pass

    def render(self):
        self.interface.draw()
        self.interface.render()
