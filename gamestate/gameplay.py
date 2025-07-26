from typing import TYPE_CHECKING

import pygame

import state
from camera import Camera
from engine import Engine
from gamestate.gamestate import GameState
from gamestate.interface.gameplay import Gameplay as Interface
from map import Map
from player import Player

if TYPE_CHECKING:
    from db import Db


class Gameplay(GameState):

    STATE_CODE = "play"
    STATE_PAUSE_CODE = "pause"

    map: Map
    camera: Camera
    player: Player
    engine: Engine

    def __init__(self):
        super().__init__()
        self.interface = Interface()
        self.map = None
        self.camera = None
        self.player = None
        self.engine = None

    def init(self, db: "Db"):
        self.map = Map()
        self.map.load_map()
        self.interface.minimap.map = self.map
        super().init(db)
        self.player = Player(db)
        self.engine = Engine(db)
        self.camera = Camera(self.player, self.interface.gaming_area, self.map)
        self.player.camera = self.camera
        self.player.load(self.map.start)
        self.engine.init(self.map, self.camera, self.player, self.interface.gaming_area)

    def check_input(self):
        super().check_input()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if state.running == self.STATE_CODE:
                        state.running = self.STATE_PAUSE_CODE
                    else:
                        state.running = self.STATE_CODE

    def update(self):
        super().update()
        if state.resize:
            self.camera.update()
            state.resize = False
        self.engine.run()

    def do_interaction(self):
        self.engine.check_collision()
        self.engine.check_is_seen()
        click, clicked = self.check_clicked_item()
        if click:
            if self.engine.check_near(clicked):
                if click == 1:
                    # todo attacca mostro
                    clicked.act(self.player, self.map.items, self.interface.dialog)  # azione contestuale principale
                    # todo parla con png
                    # todo seleziona personaggio
                elif click == 2:
                    pass
                    # todo menù attacchi secondari (pausa?)
                    # todo menù azioni contestuali oggetto, personaggio, png (pausa?)
            else:
                distance = self.engine.distance(self.player.rect.center, clicked.rect.center)
                distance
                if click == 1:
                    pass
                    # todo attacca mostro
                    # todo seleziona personaggio
                elif click == 2:
                    pass
                    # todo menù attacchi secondari (pausa?)
        # todo interazioni ambientali o particolari?

    def check_clicked_item(self):
        click = 0
        clicked = None
        if state.mouse:
            x = state.mouse["pos"][0] - self.interface.gaming_area.rect.x + self.camera.x - self.interface.gaming_area.rect.width // 2
            y = state.mouse["pos"][1] - self.interface.gaming_area.rect.y + self.camera.y - self.interface.gaming_area.rect.height // 2
            for item in self.engine.visible_items:
                if state.mouse["button"] == "left" and item.rect.collidepoint(x, y):
                    click = 1
                    clicked = item
                elif state.mouse["button"] == "right" and item.rect.collidepoint(x, y):
                    click = 2
                    clicked = item
        return click, clicked

    def animate(self):
        # todo animazioni
        pass

    def audio(self):
        # todo audio
        pass

    def render(self, error: Exception):
        self.interface.dialog.text += str(error) + "\n" if error else ""
        self.interface.draw()
        self.map.draw(self.interface.gaming_area.image, self.camera, self.engine)
        self.player.draw(self.interface.gaming_area.image, self.camera, self.map)
        self.interface.render()
