import pygame

import state
from db import Db
from camera import Camera
from map import Map


class Player(pygame.sprite.Sprite):
    
    def __init__(self, db:Db, tile_size:int):
        super().__init__()
        self.db = db
        self.tile_size = tile_size
        self.image = None
        self.rect = None
        self.back = (0, 0)
        self.info = {}
        self.stato = {}
        self.equipaggiamento = []
        self.abilita = []

    def load(self, width:int, height:int):
        try:
            #todo l'immagine deve essere legata al personaggio
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.rect = self.image.get_rect(center=(width // 2, height // 2))
            self.back = (width // 2, height // 2)
            #todo il personaggio non può satere in configurazione, dove metterlo finché non c'è il save/load?
            self.info = self.db.getOne("SELECT * FROM personaggi WHERE id = " + str(state.config["personaggio"]))
            razza = self.db.getOne("SELECT * FROM razze WHERE id = " + str(self.info["razza_id"]))
            self.info["razza"] = razza
            self.stato = self.db.getOne("SELECT * FROM stato WHERE personaggio_id = " + str(state.config["personaggio"]))
            self.equipaggiamento = self.db.get("SELECT * FROM oggetti AS o INNER JOIN equipaggiamento AS e ON e.oggetto_id = o.id WHERE e.personaggio_id = " + str(state.config["personaggio"]))
            #todo servirebbe una tabella unica, anche per gli oggetti vari
            for oggetto in self.equipaggiamento:
                if oggetto["tipo"] == "arma":
                    oggetto["caratteristiche"] = self.db.getOne("SELECT * FROM caratteristiche_armi WHERE oggetto_id = " + str(oggetto.id))
                elif oggetto["tipo"] == "armatura":
                    oggetto["caratteristiche"] = self.db.getOne("SELECT * FROM caratteristiche_armatura WHERE oggetto_id = " + str(oggetto.id))
                else:
                    oggetto["caratteristiche"] = None
            self.abilita = self.db.get("SELECT * FROM abilita AS a INNER JOIN abilita_personaggi AS p ON p.abilita_id = a.id WHERE p.personaggio_id = " + str(state.config["personaggio"]))
        except Exception as e:
            raise RuntimeError("Impossibile caricare personaggio") from e

    def update(self, kyes:pygame.key.ScancodeWrapper, width:int, height:int):
        self.back = (self.rect.centerx, self.rect.centery)
        velocita = self.info["razza"]["velocita"]
        if kyes[pygame.K_LEFT]:
            newx = self.rect.centerx - velocita
            newx = max(0, newx)
            self.rect.centerx = newx
        if kyes[pygame.K_RIGHT]:
            newx = self.rect.centerx + velocita
            newx = min(newx, width-self.tile_size)
            self.rect.centerx = newx
        if kyes[pygame.K_UP]:
            newy = self.rect.centery - velocita
            newy = max(0, newy)
            self.rect.centery = newy
        if kyes[pygame.K_DOWN]:
            newy = self.rect.centery + velocita
            newy = min(newy, height-self.tile_size)
            self.rect.centery = newy

    def go_back(self):
        self.rect.centerx = round(self.back[0] / (self.tile_size // 2)) * (self.tile_size // 2)
        self.rect.centery = round(self.back[1] / (self.tile_size // 2)) * (self.tile_size // 2)

    def draw(self, area:pygame.surface.Surface, camera:Camera, mappa:Map):
        if  camera.width // 2 < self.rect.centerx < mappa.width - camera.width // 2:
            x = area.get_rect().centerx - self.tile_size // 2
        else:
            x = self.rect.centerx - camera.x + camera.width // 2 - self.tile_size // 2
        if camera.height // 2 < self.rect.centery < mappa.height - camera.height // 2:
            y = area.get_rect().centery - self.tile_size // 2
        else:
            y = self.rect.centery - camera.y + camera.height // 2 - self.tile_size // 2
        area.blit(self.image, (x, y))