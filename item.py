import pygame

from core import GSprite


class Item(GSprite):

    def __init__(self, id: str, data: dict, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = data["pos"][0]
        self.rect.y = data["pos"][1]
        self.id = id
        self.type = data["tipo"]
        self.info = data

    def collide(
        self, target: pygame.sprite.Sprite, items: dict, dialog: pygame.sprite.Sprite
    ):
        if self.type == "porta":
            if self.info["stato"] == "chiusa":
                target.go_back()
        elif self.type == "trappola":
            if self.info["stato"] == "on":
                # todo modifica personaggio
                dialog.text += "Ahia\n"
                self.info["stato"] = "off"
        elif self.type == "iscrizione":
            target.go_back()
        elif self.type == "ostacolo":
            if self.info["stato"] == "on":
                target.go_back()
                # todo modifica personaggio
                dialog.text += "Ahia\n"
        elif self.type == "cassa":
            target.go_back()

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

    def act_sec(
        self, target: pygame.sprite.Sprite, items: dict, dialog: pygame.sprite.Sprite
    ):
        if self.type == "iscrizione":
            dialog.text += self.info["testo"] + "\n"
