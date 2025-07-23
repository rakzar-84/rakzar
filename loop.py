import traceback
from typing import TYPE_CHECKING

import pygame

import state
from camera import Camera
from db import Db
from engine import Engine
from interface import Interface
from map import Map
from player import Player

if TYPE_CHECKING:
    from screen import Screen


class Loop:

    screen: "Screen"
    clock: pygame.time.Clock
    map: Map
    interface: Interface
    camera: Camera
    player: Player
    engine: Engine
    error: Exception

    def __init__(self, screen: "Screen"):
        self.screen = screen
        self.clock = None
        self.map = None
        self.interface = None
        self.camera = None
        self.player = None
        self.engine = None
        self.error = None

    def init(self):
        self.clock = pygame.time.Clock()
        db = Db()
        db.connect()
        self.map = Map()
        self.map.load_map()
        self.interface = Interface(self.screen)
        self.interface.init()
        self.player = Player(db)
        self.engine = Engine(db)
        self.camera = Camera(self.player, self.interface.gaming_area, self.map)
        self.player.camera = self.camera
        self.player.load(self.map.start)
        self.engine.init(self.map, self.camera, self.player, self.interface.gaming_area)
        state.resize = False

    def execute(self):
        state.running = 1
        while state.running:
            try:
                state.profiler.reset()
                self.clock.tick(state.config["fps"])
                self.check_input()
                self.update()
                self.do_interaction()
                self.animate()
                self.audio()
            except Exception as e:
                print(traceback.format_exc())
                self.error = e
            self.render()

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
                    self.screen.to_window()
                    state.resize = True
                elif event.key == pygame.K_F12:
                    self.screen.to_fullscreen()
                    state.resize = True
                elif event.key == pygame.K_SPACE:
                    if state.running == 1:
                        state.running = 2
                    else:
                        state.running = 1
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
                state.running = 0

    def update(self):
        self.screen.update()
        if state.resize:
            self.interface.init()
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

    def render(self):
        try:
            self.screen.draw()
            self.interface.dialog.text += str(self.error) + "\n" if self.error else ""
            self.interface.minimap.map = self.map
            self.interface.draw()
            self.map.draw(self.interface.gaming_area.image, self.camera, self.engine)
            self.player.draw(self.interface.gaming_area.image, self.camera, self.map)
            self.interface.sprite_set.draw(self.screen.image)
            pygame.display.flip()
        except Exception as e:
            raise RuntimeError("Errore esecuzione") from e
