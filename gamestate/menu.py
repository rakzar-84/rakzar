from typing import TYPE_CHECKING

from gamestate.gamestate import GameState
from gamestate.interface.menu import Menu as Interface

if TYPE_CHECKING:
    from gamestate.interface.interface import Screen


class Menu(GameState):

    STATE_CODE = "menu"

    def __init__(self, screen: "Screen"):
        super().__init__(screen)
        self.interface = Interface(screen)
