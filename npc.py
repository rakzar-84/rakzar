import pygame

from core import GSprite
from db import Db


class Monster(GSprite):

    dg: Db
    id: str
    back: tuple
    info: dict
    state: dict
    equipment: list
    abilities: list

    def __init__(self, db: Db, id: str):
        super().__init__()
        self.db = db
        self.id = id
        self.info = {}
        self.stato = {}
        self.equipaggiamento = []
        self.abilita = []

    def load(self, info: dict):
        try:
            # qui
            # self.info = self.db.getOne("SELECT *
            # FROM personaggi
            # WHERE id = " + str(info["id"]))
            # todo l'immagine deve essere legata al mostro
            self.image = pygame.image.load(
                "assets/personaggi/monster.png"
            ).convert_alpha()  # todo ridimensionare in base alle dimensioni
            self.rect = self.image.get_rect()
            self.rect.x = info["pos"][0]
            self.rect.y = info["pos"][1]
            # razza = self.db.getOne("SELECT *
            # FROM razze
            # WHERE id = " + str(info["id"]))
            # self.info["razza"] = razza
            # self.stato = self.db.getOne("SELECT * FROM stato
            # WHERE personaggio_id = " + str(info["id"]))
            # self.equipaggiamento = self.db.get("SELECT *
            # FROM oggetti AS o
            # INNER JOIN equipaggiamento AS e ON e.oggetto_id = o.id
            # WHERE e.personaggio_id = " + str(info["id"]))
            # for oggetto in self.equipaggiamento:
            #    if oggetto["tipo"] == "arma":
            #        oggetto["caratteristiche"] = self.db.getOne("SELECT *
            # FROM caratteristiche_armi
            # WHERE oggetto_id = " + str(oggetto.id))
            #    elif oggetto["tipo"] == "armatura":
            #       oggetto["caratteristiche"] = self.db.getOne("SELECT *
            # FROM caratteristiche_armatura
            # WHERE oggetto_id = " + str(oggetto.id))
            #    else:
            #        oggetto["caratteristiche"] = None
            # self.abilita = self.db.get("SELECT *
            # FROM abilita AS a
            # INNER JOIN abilita_personaggi AS p ON p.abilita_id = a.id
            # WHERE p.personaggio_id = " + str(state.config["personaggio"]))
        except Exception as e:
            raise RuntimeError("Impossibile caricare personaggio") from e
