from typing import TYPE_CHECKING

import pygame

import state
from core import GSprite

if TYPE_CHECKING:
    from camera import Camera
    from db import Db
    from map import Map


class Npc(GSprite):

    dg: "Db"
    id: str
    back: tuple
    info: dict
    state: dict
    equipment: list
    abilities: list
    razza: dict
    alerted: bool

    def __init__(self, db: "Db"):
        super().__init__()
        self.back = (0, 0)
        self.db = db
        self.id = ""
        self.info = {}
        self.stato = {}
        self.equipaggiamento = []
        self.abilita = []
        self.razza = {}
        self.alerted = False

    def load(self, info: dict):
        try:
            self.id = info["id"]
            # todo creare i personaggi dei mostri in fase di creazione della partita
            npg = self.db.getOne(
                "SELECT * FROM npg WHERE map_id = '" + str(info["id"] + "'")
            )
            self.info = self.db.getOne(
                "SELECT * FROM personaggi WHERE id = " + str(npg["personaggio_id"])
            )
            razza = self.db.getOne(
                "SELECT * FROM razze WHERE id = " + str(self.info["razza_id"])
            )
            self.razza = razza
            dimension = razza["dimensione"] * state.config["tile_size"]
            self.state = self.db.getOne(
                "SELECT * FROM stato WHERE personaggio_id = " + str(self.info["id"])
            )
            self.equipment = self.db.get(
                "SELECT * FROM oggetti AS o INNER JOIN equipaggiamento AS e ON e.oggetto_id = o.id WHERE e.personaggio_id = "
                + str(self.info["id"])
            )
            # todo dove mettere le caratteristiche degli oggetti?
            self.abilities = self.db.get(
                "SELECT * FROM abilita AS a INNER JOIN abilita_personaggi AS p ON p.abilita_id = a.id WHERE p.personaggio_id = "
                + str(self.info["id"])
            )
            self.image = pygame.image.load(
                "assets/personaggi/" + self.info["img"]
            ).convert_alpha()  # todo ridimensionare in base alle dimensioni
            self.rect = self.image.get_rect(
                center=(
                    info["pos"][0] * (dimension // 2),
                    info["pos"][1] * (dimension // 2),
                )
            )
            self.back = self.rect.center
        except Exception as e:
            raise RuntimeError("Impossibile caricare personaggio") from e

    def move(self, x: int, y: int):
        self.back = self.rect.center
        self.rect.centerx = x
        self.rect.centery = y

    def draw(
        self, area: pygame.surface.Surface, camera: "Camera", mappa: "Map"
    ):  # todo fare
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
