import pygame
import json
from PIL import Image
from collections import Counter

import state
from db import Db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from camera import Camera


class Map:

    TILE_SIZE = 50 #todo parametrizzare

    def __init__(self):
        self.map_tiles = []
        self.tiles_images = []
        self.tiles_types = {}
        self.visible_tiles = pygame.sprite.Group()
        self.visible_wall = pygame.sprite.Group()
        self.blocchi_x = 0
        self.blocchi_y = 0
        self.width = 0
        self.height = 0
        self.items = {}
        self.visible_items = pygame.sprite.Group()

    def load_map(self):
        try:
            immagine = Image.open(state.config['mappa'] + "mappa.png").convert("RGB")
            self.width, self.height = immagine.size
            self.blocchi_x = self.width // self.TILE_SIZE
            self.blocchi_y = self.height // self.TILE_SIZE
            self.load_tiles_images()
            self.load_tiles_type()
            for by in range(self.blocchi_y):
                riga = []
                for bx in range(self.blocchi_x):
                    blocco = immagine.crop((bx * self.TILE_SIZE, by * self.TILE_SIZE, (bx + 1) * self.TILE_SIZE, (by + 1) * self.TILE_SIZE))
                    pixel_data = list(blocco.getdata())
                    colore = Counter(pixel_data).most_common(1)[0][0]
                    hex = '#{:02X}{:02X}{:02X}'.format(*colore)
                    riga.append(self.tiles_types[hex])
                self.map_tiles.append(riga)
            self.load_items()
        except Exception as e:
            raise RuntimeError("Caricamento mappa non riuscito") from e

    def load_tiles_images(self):
        pil_immagine = Image.open(state.config['mappa'] + "tilesheet.png").convert("RGB")
        w, h = pil_immagine.size
        tiles_x = w // self.TILE_SIZE
        tiles_y = h // self.TILE_SIZE
        immagine = pygame.image.fromstring(pil_immagine.tobytes(), pil_immagine.size, pil_immagine.mode)
        for index in range(tiles_x * tiles_y):
            x = (index % tiles_x) * self.TILE_SIZE
            y = (index // tiles_x) * self.TILE_SIZE
            tile_img = immagine.subsurface(pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)).copy()
            self.tiles_images.append(tile_img)

    def load_tiles_type(self):
        with open(state.config['mappa'] + "types.json", 'r', encoding='utf-8') as file:
            self.tiles_types = json.load(file)

    def load_items(self):
        with open(state.config['mappa'] + "items.json", 'r', encoding='utf-8') as file:
            items = json.load(file)
            for id, item in items.items():
                oggetto = Item(id, item, self.tiles_images)
                self.items[id] = oggetto

    def update(self, camera:"Camera"):
        self.visible_tiles.empty()
        self.visible_wall.empty()
        tile_visibili_x = camera.width // self.TILE_SIZE + 2
        tile_visibili_y = camera.height // self.TILE_SIZE + 2
        camera_left = camera.x - camera.width // 2
        camera_top = camera.y - camera.height // 2
        tile_start_x = camera_left // self.TILE_SIZE
        tile_start_y = camera_top // self.TILE_SIZE
        for y in range(tile_start_y, tile_start_y + tile_visibili_y):
            for x in range(tile_start_x, tile_start_x + tile_visibili_x):
                if 0 <= x < self.blocchi_x and 0 <= y < self.blocchi_y:
                    tile = self.map_tiles[y][x]
                    img_tile = self.tiles_images[tile["type"]]
                    rect_tile = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    tile = Tile(img_tile, rect_tile, tile["type"], tile["muro"])
                    self.visible_tiles.add(tile)
                    if tile.wall:
                        self.visible_wall.add(tile)
                for item in self.items.values():
                    item_tile_x = item.rect.x // self.TILE_SIZE
                    item_tile_y = item.rect.y // self.TILE_SIZE
                    if x == item_tile_x and y == item_tile_y:
                        self.visible_items.add(item)

    def draw(self, area:pygame.Surface, camera:"Camera"):
        camera_left = camera.x - camera.width // 2
        camera_top = camera.y - camera.height // 2
        for tile in self.visible_tiles:
            rect_area = tile.rect.move(-camera_left, -camera_top)
            area.blit(tile.image, rect_area)
        for item in self.visible_items:
            rect_area = item.rect.move(-camera_left, -camera_top)
            area.blit(item.image, rect_area)



class Tile(pygame.sprite.Sprite):

    def __init__(self, image:pygame.surface.Surface, rect:pygame.Rect, type:int, muro:bool):
        super().__init__()
        self.image = image
        self.rect = rect
        self.type = type
        self.wall = muro


class Item(pygame.sprite.Sprite):

    def __init__(self, id:str, data:dict, tiles_images:list):
        super().__init__()
        self.image = tiles_images[data["img"]]
        self.rect = self.image.get_rect()
        self.rect.x = data["pos"][0]
        self.rect.y = data["pos"][1]
        self.id = id
        self.type = data["tipo"]
        self.info = data

    def collide(self, target:pygame.sprite.Sprite, items:dict, dialog:pygame.sprite.Sprite):
        if self.type == "porta":
            if self.info["stato"] == "chiusa":
                target.go_back()
        elif self.type == "trappola":
            if self.info["stato"] == "on":
                #todo modifica personaggio
                dialog.text += "Ahia"
                self.info["stato"] = "off"
        elif self.type == "iscrizione":
                target.go_back()
        elif self.type == "ostacolo":
            if self.info["stato"] == "on":
                target.go_back()
                #todo modifica personaggio
                dialog.text += "Ahia"
        elif self.type == "cassa":
            target.go_back()

    def act(self, target:pygame.sprite.Sprite, items:dict, dialog:pygame.sprite.Sprite):
        if self.type == "leva":
            if self.info["stato"] == "off":
                self.info["stato"] = "on"
                items[self.info["target"]].info["stato"] = "aperta"
            else:
                items[self.info["target"]].info["stato"] = "chiusa"
                self.info["stato"] = "off"
        elif self.type == "iscrizione":
                dialog.text += self.info["testo"] + "\n"
        elif self.type == "cassa":
            #todo scelta oggetto da usare
            #todo come gestisco diverse azioni?
            #qui
