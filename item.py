from typing import TYPE_CHECKING

import pygame

from core import GSprite

if TYPE_CHECKING:
    from engine import Engine
    from npc import Npc
    from player import Player


class Item(GSprite):

    def __init__(self, id: str, data: dict, image: pygame.Surface, rect: pygame.Rect):
        super().__init__()
        self.image = image
        self.rect = rect
        self.rect.x = data["pos"][0]
        self.rect.y = data["pos"][1]
        self.id = id
        self.type = data["tipo"]
        self.info = data

    def collide(self, player: "Player", engine: "Engine", dialog: pygame.sprite.Sprite):
        if self.type == "porta":
            if self.info["stato"] == "chiusa":
                engine.go_back_player()
        elif self.type == "trappola":
            if self.info["stato"] == "on":
                # todo modifica personaggio
                dialog.text += "Ahia\n"
                self.info["stato"] = "off"
        elif self.type == "iscrizione":
            engine.go_back_player()
        elif self.type == "ostacolo":
            if self.info["stato"] == "on":
                engine.go_back_player()
                # todo modifica personaggio
                dialog.text += "Ahia\n"
        elif self.type == "cassa":
            engine.go_back_player()

    def collide_npc(self, npc: "Npc", engine: "Engine"):
        if self.type == "porta":
            if self.info["stato"] == "chiusa":
                engine.go_back_npc(npc)
        elif self.type == "trappola":
            if self.info["stato"] == "on":
                # todo modifica npc
                self.info["stato"] = "off"
        elif self.type == "iscrizione":
            engine.go_back_npc(npc)
        elif self.type == "ostacolo":
            if self.info["stato"] == "on":
                engine.go_back_npc(npc)
                # todo modifica npc
        elif self.type == "cassa":
            engine.go_back_npc(npc)

    def act(
        self, target: pygame.sprite.Sprite, items: dict, dialog: pygame.sprite.Sprite
    ):
        if self.type == "leva":
            if self.info["stato"] == "off":
                self.info["stato"] = "on"
                items[self.info["target"]].info["stato"] = "aperta"
                dialog.text += "Leva on\n"
            else:
                items[self.info["target"]].info["stato"] = "chiusa"
                self.info["stato"] = "off"
                dialog.text += "Leva off\n"
        elif self.type == "cassa":
            if self.info["stato"] == "aperta":
                # todo  mostra contenuto (pausa)
                dialog.text += "Contenuto\n"
            else:
                # todo scelta oggetto da usare (pausa)
                dialog.text += "Usa chiave"
        elif self.type == "oggetto":
            target.add_item(self)
            del items[self.id]
            dialog.text += "Oggetto raccolto\n"
