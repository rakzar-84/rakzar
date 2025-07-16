import pygame
import traceback

import state
from interfaccia import Interfaccia
from map import Map, Item
from player import Player
from camera import Camera
from db import Db
from screen import Screen


class Loop:

    def __init__(self, screen:Screen):
        self.screen = screen
        self.clock = None
        self.mappa = None
        self.interfaccia = None
        self.camera = None
        self.player = None
        self.errore = None
        self.resize = True
        self.click = ()

    def init(self):
        self.clock = pygame.time.Clock()
        db = Db()
        db.connect()
        self.mappa = Map()
        self.mappa.load_map()
        self.interfaccia = Interfaccia(self.screen)
        self.player = Player(db, self.mappa.TILE_SIZE)
        self.player.load(self.mappa.width, self.mappa.height)
        self.camera = Camera(self.player, self.interfaccia.gaming_area, self.mappa)

    def execute(self):
        state.vars["running"] = True
        while state.vars["running"]:
            try:
                self.clock.tick(state.config["fps"])
                self.check_input()
                self.update()
                self.do_interaction()
                self.animate()
                self.audio()
            except Exception as e:
                print(traceback.format_exc())
                self.errore = e
            self.render()

    def check_input(self):
        self.click = ()
        for event in pygame.event.get():
            #todo quali altri eventi?
            #MOUSEWHEEL
            #USEREVENT
            #TEXTINPUT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.screen.to_window()
                    self.resize = True
                elif event.key == pygame.K_F12:
                    self.screen.to_fullscreen()
                    self.resize = True
            if event.type == pygame.VIDEORESIZE:
                self.resize = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = event.pos
            if event.type == pygame.QUIT:
                state.vars["running"] = False
        state.vars["keys"] = pygame.key.get_pressed()

    def update(self):
        self.screen.update(self.resize)
        self.interfaccia.update(self.resize)
        self.resize = False
        self.player.update(state.vars["keys"], self.mappa.width, self.mappa.height)
        self.camera.update()
        self.mappa.update(self.camera)

    def do_interaction(self):
        collisi = pygame.sprite.spritecollide(self.player, self.mappa.visible_wall, False)
        if collisi:
            self.player.go_back()
        dist = 8 #todo parametrizzare?
        for item in self.mappa.visible_items:
            if self.player.rect.colliderect(item.rect):
                item.collide(self.player, self.mappa.items, self.interfaccia.dialog)
            if self.click:
                x = self.click[0] - self.interfaccia.gaming_area.rect.x + self.camera.x - self.interfaccia.gaming_area.rect.width // 2
                y = self.click[1] - self.interfaccia.gaming_area.rect.y + self.camera.y - self.interfaccia.gaming_area.rect.height // 2
                if item.rect.collidepoint(x, y):
                    if self.player.rect.colliderect(item.rect.inflate(dist, dist)):
                        item.act(self.player, self.mappa.items, self.interfaccia.dialog)

    def animate(self):
        #todo animazioni
        pass

    def audio(self):
        #todo audio
        pass

    def render(self):
        try:
            #todo usare una cache per non ricreare sempre tutte le surface/sprite
            self.screen.draw()
            self.interfaccia.dialog.text += str(self.errore) + "\n" if self.errore else ''
            self.interfaccia.draw()
            self.mappa.draw(self.interfaccia.gaming_area.image, self.camera)
            self.player.draw(self.interfaccia.gaming_area.image, self.camera, self.mappa)
            self.interfaccia.sprite_set.draw(self.screen.surface)
            pygame.display.flip()
        except Exception as e:
            raise RuntimeError("Errore esecuzione") from e
