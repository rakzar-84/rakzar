import pygame

import state
from core import GSprite
from db import Db


class Npc(GSprite):

    dg: Db
    id: str
    back: tuple
    info: dict
    state: dict
    equipment: list
    abilities: list

    def __init__(self, db: Db):
        super().__init__()
        self.db = db
        self.id = ""
        self.info = {}
        self.stato = {}
        self.equipaggiamento = []
        self.abilita = []

    def load(self, info: dict):
        try:
            self.id = self.info["id"]
            # todo creare i personaggi dei mostri in fase di creazione della partita
            npg = (
                self.db.getOne(
                    "SELECT * FROM npg WHERE map_id = '" + str(self.info["id"])
                )
                + "'"
            )
            self.info = self.db.getOne(
                "SELECT * FROM personaggi WHERE id = " + npg["personaggio_id"]
            )
            razza = self.db.getOne(
                "SELECT * FROM razze WHERE id = " + str(self.info["razza_id"])
            )
            self.info["razza"] = razza
            dimension = razza["dimensione"] * state.config["tile_size"]
            self.state = self.db.getOne(
                "SELECT * FROM stato WHERE personaggio_id = "
                + str(state.config["personaggio"])
            )
            self.equipment = self.db.get(
                "SELECT * FROM oggetti AS o INNER JOIN equipaggiamento AS e ON e.oggetto_id = o.id WHERE e.personaggio_id = "
                + str(self.info["personaggio"])
            )
            # todo dove mettere le caratteristiche degli oggetti?
            self.abilities = self.db.get(
                "SELECT * FROM abilita AS a INNER JOIN abilita_personaggi AS p ON p.abilita_id = a.id WHERE p.personaggio_id = "
                + str(self.info["personaggio"])
            )
            self.image = pygame.image.load(
                "assets/personaggi" + self.info["img"]
            ).convert_alpha()  # todo ridimensionare in base alle dimensioni
            self.rect = self.image.get_rect(
                center=(
                    info["pos"][0] * (dimension // 2),
                    info["pos"][1] * (dimension // 2),
                )
            )
        except Exception as e:
            raise RuntimeError("Impossibile caricare personaggio") from e
