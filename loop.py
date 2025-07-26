import traceback
from typing import TYPE_CHECKING

import pygame

import state
from db import Db
from gamestate.gameplay import Gameplay

if TYPE_CHECKING:
    from gamestate.gamestate import GameState


class Loop:
    clock: pygame.time.Clock
    error: Exception
    gamestate: "GameState"

    def __init__(self):
        self.clock = None
        self.error = None
        self.gamestate = None

    def init(self):
        self.clock = pygame.time.Clock()
        db = Db()
        db.connect()
        # debug mettere Menu o altro
        self.gamestate = Gameplay()
        self.gamestate.init(db)
        state.resize = False

    def execute(self):
        state.running = self.gamestate.STATE_CODE
        while state.running:
            try:
                state.profiler.reset()
                self.clock.tick(state.config["fps"])
                self.gamestate.check_input()
                self.gamestate.update()
                self.gamestate.do_interaction()
                self.gamestate.animate()
                self.gamestate.audio()
            except Exception as e:
                print(traceback.format_exc())
                self.error = e
            try:
                self.gamestate.render(self.error)
                pygame.display.flip()
            except Exception as e:
                raise RuntimeError("Errore esecuzione") from e
