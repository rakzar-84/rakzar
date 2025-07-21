import math
from typing import TYPE_CHECKING

import pygame

import state
from item import Item
from map import Tile
from npc import Npc

if TYPE_CHECKING:
    from camera import Camera
    from core import GSprite
    from db import Db
    from interface import GamingArea
    from map import Map
    from player import Player


class Engine:

    db: "Db"
    map: "Map"
    camera: "Camera"
    player: "Player"
    gaming_area: "GamingArea"
    visible_path: pygame.sprite.Group
    visible_not_path: pygame.sprite.Group
    visible_items: pygame.sprite.Group
    visible_npc: pygame.sprite.Group

    def __init__(self, db: "Db"):
        self.db = db
        self.map = None
        self.camera = None
        self.player = None
        self.gaming_area = None
        self.visible_path = pygame.sprite.Group()
        self.visible_not_path = pygame.sprite.Group()
        self.visible_items = pygame.sprite.Group()
        self.visible_npc = pygame.sprite.Group()

    def init(
        self, map: "Map", camera: "Camera", player: "Player", gamin_area: "GamingArea"
    ):
        self.map = map
        self.camera = camera
        self.player = player
        self.gaming_area = gamin_area

    def run(self):
        self.move_player()
        self.load_visible_area()
        self.move_visible_monster()

    def move_player(self):
        # todo amovimento con il click
        newx = self.player.rect.centerx
        newy = self.player.rect.centery
        if state.keys[pygame.K_LEFT]:
            newx = self.player.rect.centerx - self.player.info["razza"]["velocita"]
            newx = max(0, newx)
        if state.keys[pygame.K_RIGHT]:
            newx = self.player.rect.centerx + self.player.info["razza"]["velocita"]
            newx = min(newx, self.map.width - state.config["tile_size"])
        if state.keys[pygame.K_UP]:
            newy = self.player.rect.centery - self.player.info["razza"]["velocita"]
            newy = max(0, newy)
        if state.keys[pygame.K_DOWN]:
            newy = self.player.rect.centery + self.player.info["razza"]["velocita"]
            newy = min(newy, self.map.height - state.config["tile_size"])
        self.player.move(newx, newy)

    def go_back_player(self):
        newx = round(self.player.back[0] / (state.config["tile_size"] // 2)) * (
            state.config["tile_size"] // 2
        )
        newy = round(self.player.back[1] / (state.config["tile_size"] // 2)) * (
            state.config["tile_size"] // 2
        )
        self.player.move(newx, newy)

    def load_visible_area(self):
        self.visible_path.empty()
        self.visible_not_path.empty()
        self.visible_items.empty()
        self.visible_npc.empty()
        tile_visibili_x = self.camera.width // state.config["tile_size"] + 2
        tile_visibili_y = self.camera.height // state.config["tile_size"] + 2
        camera_left = self.camera.x - self.camera.width // 2
        camera_top = self.camera.y - self.camera.height // 2
        tile_start_x = camera_left // state.config["tile_size"]
        tile_start_y = camera_top // state.config["tile_size"]
        for y in range(tile_start_y, tile_start_y + tile_visibili_y):
            for x in range(tile_start_x, tile_start_x + tile_visibili_x):
                if 0 <= x < self.map.blocchi_x and 0 <= y < self.map.blocchi_y:
                    tile = self.map.tiled_map[y][x]
                    img_tile = self.map.tiles_images[tile["type"]]
                    rect_tile = pygame.Rect(
                        x * state.config["tile_size"],
                        y * state.config["tile_size"],
                        state.config["tile_size"],
                        state.config["tile_size"],
                    )
                    tile = Tile(img_tile, rect_tile, tile["type"], tile["cat"])
                    # todo tipi tile
                    # path: visione, movimento
                    # wall:
                    # ostacolo: visione
                    # oscuramento: movimento
                    if tile.cat == "wall":
                        self.visible_not_path.add(tile)
                    else:
                        self.visible_path.add(tile)
                for item in self.map.items.values():
                    image = self.map.tiles_images[item["img"]]
                    rect = image.get_rect()
                    item_tile_x = rect.x // state.config["tile_size"]
                    item_tile_y = rect.y // state.config["tile_size"]
                    if x == item_tile_x and y == item_tile_y:
                        self.visible_items.add(Item(id, item, image, rect))
                for npc in self.map.npc:
                    npc_sprite = Npc(self.db)
                    npc_sprite.load(npc)
                    npc_tile_x = npc_sprite.rect.x // state.config["tile_size"]
                    npc_tile_y = npc_sprite.rect.y // state.config["tile_size"]
                    if x == npc_tile_x and y == npc_tile_y:
                        self.visible_npc.add(npc_sprite)

    def move_visible_monster(self):
        for npc in self.visible_npc:
            if npc.info["tipo"] == "Mostro":
                self.move_monster(npc)

    def move_monster(self, npc: Npc):
        last_target = None
        nop = 0
        path = []
        now = pygame.time.get_ticks()
        if not path or last_target != self.player.rect.center or now - nop > 1000:
            path = self.bfs(npc.rect.center, self.player.rect.center)
            last_target = self.player.rect.center
            nop = now
        self.follow_path(npc, path)

    def bresenham(self, start: tuple, end: tuple):
        goal = False
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        line = []
        while not goal:
            line.append((x0, y0))
            if (x0, y0) == (x1, y1):
                goal = True
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return line

    def bfs(self, map: "Map", start: tuple, end: tuple):
        queue = [start]
        visited = {start: None}
        goal = False
        while not goal:
            corrente = queue.pop(0)
            if corrente == end:
                goal = True
            for vic in self.near_path(map, corrente):
                if vic not in visited:
                    visited[vic] = corrente
                    queue.append(vic)
        path = []
        pos = end
        while pos and pos in visited:
            path.append(pos)
            pos = visited[pos]
        path.reverse()
        return path

    def near_path(self, map: "Map", pos: tuple):
        x, y = pos
        adiacenti = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        # considerare item e altro
        return [p for p in adiacenti if not map[p[1]][p[0]]["cat"] == "wall"]

    def follow_path(self, subject: "GSprite", path: list):
        if path:
            next = self.path[0]
            if next != subject.rect.center:
                subject.move(next[0], next[1])
                path.pop(0)

    def distance(self, a: tuple, b: tuple):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def can_show(self, start: tuple, end: tuple):
        check = True
        for x, y in self.bresenham(start, end):
            if self.map.tiled_map[y][x]["cat"] == "wall":
                check = False
        return check

    def go_back_npc(self, npc: Npc):
        newx = round(npc.back[0] / (state.config["tile_size"] // 2)) * (
            state.config["tile_size"] // 2
        )
        newy = round(npc.back[1] / (state.config["tile_size"] // 2)) * (
            state.config["tile_size"] // 2
        )
        npc.move(newx, newy)

    def check_collision(self):
        collisioni = pygame.sprite.spritecollide(
            self.player, self.visible_not_path, False
        )
        if collisioni:
            self.go_back_player()
        collisioni = pygame.sprite.spritecollide(self.player, self.visible_npc, False)
        if collisioni:
            self.go_back_player()  # todo chi va indietro?
        for npc in self.visible_npc:
            if npc.info["tipo"] == "Mostro":
                collisioni = pygame.sprite.spritecollide(
                    npc, self.visible_not_path, False
                )
                if collisioni:
                    self.go_back_npc()

    def check_is_seen(self):
        for npc in self.visible_npc:
            if (
                self.distance(npc.rect.center, self.player.rect.center)
                <= npc.razza["vista"]
            ):
                # todo considerare effetti player (invidibilità)
                if self.can_show(npc.rect.center, self.player.rect.center):
                    npc.alerted = True
                    npc.act_alerted()  # todo i mostri attaccano

    def check_near(self, target: "GSprite"):
        dist = 8  # todo parametrizzare?
        is_near = self.player.rect.colliderect(target.rect.inflate(dist, dist))
        return is_near

    def subject(self, subject: "GSprite", target: "GSprite"):
        distance = self.distance(subject.rect.center, target.rect.center)
        is_within_range = subject.subject(distance)
        return is_within_range
