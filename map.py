import json
from collections import Counter
from typing import TYPE_CHECKING

import pygame
from PIL import Image

import state
from core import GSprite

if TYPE_CHECKING:
    from camera import Camera


class Map:

    blocchi_x: int
    blocchi_y: int
    width: int
    height: int
    tiled_map: list
    start: tuple
    tiles_images: list
    tiles_types: dict
    items: dict
    monsters: dict

    def __init__(self):
        self.width = 0
        self.height = 0
        self.blocchi_x = 0
        self.blocchi_y = 0
        self.tiled_map = []
        self.start = (0, 0)
        self.tiles_images = []
        self.tiles_types = {}
        self.items = {}
        self.monsters = {}

        self.visible_tiles = pygame.sprite.Group()
        self.visible_wall = pygame.sprite.Group()
        self.visible_items = pygame.sprite.Group()
        self.visible_monsters = pygame.sprite.Group()

    def load_map(self):
        try:
            immagine = Image.open(state.config["mappa"] + "mappa.png").convert("RGB")
            self.width, self.height = immagine.size
            self.blocchi_x = self.width // state.config["tile_size"]
            self.blocchi_y = self.height // state.config["tile_size"]
            self.load_tiles_images()
            self.load_tiles_type()
            for by in range(self.blocchi_y):
                riga = []
                for bx in range(self.blocchi_x):
                    blocco = immagine.crop(
                        (
                            bx * state.config["tile_size"],
                            by * state.config["tile_size"],
                            (bx + 1) * state.config["tile_size"],
                            (by + 1) * state.config["tile_size"],
                        )
                    )
                    pixel_data = list(blocco.getdata())
                    colore = Counter(pixel_data).most_common(1)[0][0]
                    hex = "#{:02X}{:02X}{:02X}".format(*colore)
                    riga.append(self.tiles_types[hex])
                    if hex == "#404040":
                        self.start = (bx, by)
                self.tiled_map.append(riga)
            self.load_items()
            self.load_mostri()
        except Exception as e:
            raise RuntimeError("Caricamento mappa non riuscito") from e

    def load_tiles_images(self):
        pil_immagine = Image.open(state.config["mappa"] + "tilesheet.png").convert(
            "RGB"
        )
        w, h = pil_immagine.size
        tiles_x = w // state.config["tile_size"]
        tiles_y = h // state.config["tile_size"]
        immagine = pygame.image.fromstring(
            pil_immagine.tobytes(), pil_immagine.size, pil_immagine.mode
        )
        for index in range(tiles_x * tiles_y):
            x = (index % tiles_x) * state.config["tile_size"]
            y = (index // tiles_x) * state.config["tile_size"]
            tile_img = immagine.subsurface(
                pygame.Rect(x, y, state.config["tile_size"], state.config["tile_size"])
            ).copy()
            self.tiles_images.append(tile_img)

    def load_tiles_type(self):
        with open(state.config["mappa"] + "types.json", "r", encoding="utf-8") as file:
            self.tiles_types = json.load(file)

    def load_items(self):
        with open(state.config["mappa"] + "items.json", "r", encoding="utf-8") as file:
            self.items = json.load(file)

    def load_mostri(self):
        with open(state.config["mappa"] + "mostri.json", "r", encoding="utf-8") as file:
            self.monsters = json.load(file)

    def draw(self, area: pygame.Surface, camera: "Camera"):
        camera_left = camera.x - camera.width // 2
        camera_top = camera.y - camera.height // 2
        for tile in self.visible_tiles:
            rect_area = tile.rect.move(-camera_left, -camera_top)
            area.blit(tile.image, rect_area)
        for item in self.visible_items:
            rect_area = item.rect.move(-camera_left, -camera_top)
            area.blit(item.image, rect_area)
        for monster in self.visible_monsters:
            rect_area = monster.rect.move(-camera_left, -camera_top)
            area.blit(monster.image, rect_area)


class Tile(GSprite):

    def __init__(
        self, image: pygame.surface.Surface, rect: pygame.Rect, type: int, muro: bool
    ):
        super().__init__()
        self.image = image
        self.rect = rect
        self.type = type
        self.wall = muro
