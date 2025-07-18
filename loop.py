import traceback

import pygame

import state
from camera import Camera
from db import Db
from engine import Engine
from interface import Interface
from map import Map
from player import Player
from screen import Screen


class Loop:

    screen: Screen
    clock: pygame.time.Clock
    map: Map
    interface: Interface
    camera: Camera
    player: Player
    engine: Engine
    error: Exception
    resize: bool

    def __init__(self, screen: Screen):
        self.screen = screen
        self.clock = None
        self.map = None
        self.interface = None
        self.camera = None
        self.player = None
        self.engine = None
        self.error = None
        # todo è solo un'inormazione trasmessa da un metodo ad un altro, va bene?
        self.resize = True

    def init(self):
        self.clock = pygame.time.Clock()
        db = Db()
        db.connect()
        self.map = Map()
        self.map.load_map()
        self.interface = Interface(self.screen)
        self.player = Player(db)
        self.player.load(self.map.width, self.map.height)
        self.camera = Camera(self.player, self.interface.gaming_area, self.map)
        self.player.camera = self.camera
        self.engine.init(
            db, self.map, self.camera, self.player, self.interface.gaming_area
        )

    def execute(self):
        state.running = 1
        while state.running:
            try:
                self.clock.tick(state.config["fps"])
                self.check_input()
                self.update()
                self.do_interaction()
                # todo serve nuovo update?
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
                    self.resize = True
                elif event.key == pygame.K_F12:
                    self.screen.to_fullscreen()
                    self.resize = True
                elif event.key == pygame.K_SPACE:
                    if state.running == 1:
                        state.running = 2
                    else:
                        state.running = 1
            if event.type == pygame.VIDEORESIZE:
                self.resize = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                state.mouse["pos"] = event.pos
                if event.button == 1:
                    state.mouse["button"] = "left"
                elif event.button == 3:
                    state.mouse["button"] = "right"
            if event.type == pygame.QUIT:
                state.running = 0

    def update(self):
        self.screen.update(self.resize)
        self.interface.update(self.resize)
        self.engine.run(self.resize)
        self.resize = False

    def do_interaction(self):  # qui
        collisi = pygame.sprite.spritecollide(self.player, self.map.visible_wall, False)
        if collisi:
            self.player.go_back()
        dist = 8  # todo parametrizzare?
        for item in self.map.visible_items:
            if self.player.rect.colliderect(item.rect):
                item.collide(self.player, self.map.items, self.interface.dialog)
                # todo collide mostro
            if state.mouse:
                x = (
                    state.mouse["pos"][0]
                    - self.interface.gaming_area.rect.x
                    + self.camera.x
                    - self.interface.gaming_area.rect.width // 2
                )
                y = (
                    state.mouse["pos"][1]
                    - self.interface.gaming_area.rect.y
                    + self.camera.y
                    - self.interface.gaming_area.rect.height // 2
                )
                if state.mouse["button"] == "left" and item.rect.collidepoint(x, y):
                    if self.player.rect.colliderect(item.rect.inflate(dist, dist)):
                        item.act(self.player, self.map.items, self.interface.dialog)
                        # todo attacca mostro
                elif state.mouse["button"] == "right" and item.rect.collidepoint(x, y):
                    if self.player.rect.colliderect(item.rect.inflate(dist, dist)):
                        item.act_sec(self.player, self.map.items, self.interface.dialog)
                        # todo menù azioni su mostro (pausa)

    def animate(self):
        # todo animazioni
        pass

    def audio(self):
        # todo audio
        pass

    def render(self):
        try:
            # todo usare una cache per non ricreare sempre tutte le surface/sprite
            self.screen.draw()
            self.interface.dialog.text += str(self.error) + "\n" if self.error else ""
            self.interface.draw()
            self.map.draw(self.interface.gaming_area.image, self.camera)
            self.player.draw(self.interface.gaming_area.image, self.camera, self.map)
            self.interface.sprite_set.draw(self.screen.image)
            pygame.display.flip()
        except Exception as e:
            raise RuntimeError("Errore esecuzione") from e
