import pygame

import state
from camera import Camera
from core import GSprite
from db import Db
from item import Item
from map import Map


class Player(GSprite):

    dg: Db
    camera: Camera
    back: tuple
    info: dict
    state: dict
    equipment: list
    abilities: list

    def __init__(self, db: Db):
        super().__init__()
        self.db = db
        self.camera = None
        self.back = (0, 0)
        self.info = {}
        self.state = {}
        self.equipment = []
        self.abilities = []

    def load(self, start: tuple):
        try:
            # todo più di un immagine
            self.image = pygame.image.load(
                "assets/personaggi/player.png"
            ).convert_alpha()  # todo ridimensionare in base alle dimensioni
            self.rect = self.image.get_rect(
                center=(
                    start[0] * (state.config["tile_size"] // 2),
                    start[1] * (state.config["tile_size"] // 2),
                )
            )
            self.back = self.rect.center
            self.info = self.db.getOne("SELECT * FROM personaggi WHERE main = 1")
            razza = self.db.getOne(
                "SELECT * FROM razze WHERE id = " + str(self.info["razza_id"])
            )
            self.info["razza"] = razza
            self.state = self.db.getOne(
                "SELECT * FROM stato WHERE personaggio_id = "
                + str(state.config["personaggio"])
            )
            self.equipment = self.db.get(
                "SELECT * FROM oggetti AS o "
                "INNER JOIN equipaggiamento AS e ON e.oggetto_id = o.id "
                "WHERE e.personaggio_id = " + str(state.config["personaggio"])
            )
            # todo servirebbe una tabella unica, anche per gli oggetti vari
            for item in self.equipment:
                if item["tipo"] == "arma":
                    item["caratteristiche"] = self.db.getOne(
                        "SELECT * FROM caratteristiche_armi WHERE oggetto_id = "
                        + str(item.id)
                    )
                elif item["tipo"] == "armatura":
                    item["caratteristiche"] = self.db.getOne(
                        "SELECT * FROM caratteristiche_armatura WHERE oggetto_id = "
                        + str(item.id)
                    )
                else:
                    item["caratteristiche"] = None
            self.abilities = self.db.get(
                "SELECT * FROM abilita AS a "
                "INNER JOIN abilita_personaggi AS p ON p.abilita_id = a.id "
                "WHERE p.personaggio_id = " + str(state.config["personaggio"])
            )
        except Exception as e:
            raise RuntimeError("Impossibile caricare personaggio") from e

    def move(self, x: int, y: int):
        self.back = self.rect.center
        self.rect.centerx = x
        self.rect.centery = y
        self.camera.update()

    def draw(self, area: pygame.surface.Surface, camera: Camera, mappa: Map):
        if camera.width // 2 < self.rect.centerx < mappa.width - camera.width // 2:
            x = area.get_rect().centerx - state.config["tile_size"] // 2
        else:
            x = (
                self.rect.centerx
                - camera.x
                + camera.width // 2
                - state.config["tile_size"] // 2
            )
        if camera.height // 2 < self.rect.centery < mappa.height - camera.height // 2:
            y = area.get_rect().centery - state.config["tile_size"] // 2
        else:
            y = (
                self.rect.centery
                - camera.y
                + camera.height // 2
                - state.config["tile_size"] // 2
            )
        area.blit(self.image, (x, y))

    def add_item(self, item: Item):
        # todo rivedere tabella equipaggiamento
        self.equipment.append(
            {
                "nome": item.id,
                "oggetto": item.info["sottotipo"],
                "qta": 1,
                "slot": "zaino",
            }
        )
