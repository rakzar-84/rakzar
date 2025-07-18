import math

import pygame

import state
from camera import Camera
from db import Db
from interface import GamingArea
from item import Item
from map import Map, Tile
from npc import Monster
from player import Player


class Engine:

    db: Db
    map: Map
    camera: Camera
    player: Player
    gaming_area: GamingArea
    visible_path: pygame.sprite.Group
    visible_not_path: pygame.sprite.Group
    visible_items: pygame.sprite.Group
    visible_monsters: pygame.sprite.Group

    def __init__(self, db: Db):
        self.db = db
        self.map = None
        self.camera = None
        self.player = None
        self.gaming_area = None
        self.visible_path = pygame.sprite.Group()
        self.visible_not_path = pygame.sprite.Group()
        self.visible_items = pygame.sprite.Group()
        self.visible_monsters = pygame.sprite.Group()

    def init(self, map: Map, camera: Camera, player: Player, gamin_area: GamingArea):
        self.map = map
        self.camera = camera
        self.player = player
        self.gaming_area = gamin_area

    def run(self, resize: bool):
        self.move_player(resize)
        self.load_visible_area(self.camera, self.player)

    def move_player(self, resize: bool):
        if state.keys[pygame.K_LEFT]:
            newx = self.player.rect.centerx - self.player.info["razza"]["velocita"]
            newx = max(0, newx)
        if state.keys[pygame.K_RIGHT]:
            newx = self.player.rect.centerx + self.player.info["razza"]["velocita"]
            newx = min(newx, self.map.width - Map.TILE_SIZE)
        if state.keys[pygame.K_UP]:
            newy = self.player.rect.centery - self.player.info["razza"]["velocita"]
            newy = max(0, newy)
        if state.keys[pygame.K_DOWN]:
            newy = self.player.rect.centery + self.player.info["razza"]["velocita"]
            newy = min(newy, self.map.height - Map.TILE_SIZE)
        self.player.move(resize, newx, newy)

    def go_back_player(self):
        newx = round(self.player.back[0] / (Map.TILE_SIZE // 2)) * (Map.TILE_SIZE // 2)
        newy = round(self.player.back[1] / (Map.TILE_SIZE // 2)) * (Map.TILE_SIZE // 2)
        self.player.move(newx, newy)

    def load_visible_area(self):
        self.visible_path.empty()
        self.visible_not_path.empty()
        self.visible_items.empty()
        self.visible_monsters.empty()
        tile_visibili_x = self.camera.width // Map.TILE_SIZE + 2
        tile_visibili_y = self.camera.height // Map.TILE_SIZE + 2
        camera_left = self.camera.x - self.camera.width // 2
        camera_top = self.camera.y - self.camera.height // 2
        tile_start_x = camera_left // Map.TILE_SIZE
        tile_start_y = camera_top // Map.TILE_SIZE
        for y in range(tile_start_y, tile_start_y + tile_visibili_y):
            for x in range(tile_start_x, tile_start_x + tile_visibili_x):
                if 0 <= x < self.map.blocchi_x and 0 <= y < self.map.blocchi_y:
                    tile = self.map.tiled_map[y][x]
                    img_tile = self.map.tiles_images[tile["type"]]
                    rect_tile = pygame.Rect(
                        x * Map.TILE_SIZE,
                        y * Map.TILE_SIZE,
                        Map.TILE_SIZE,
                        Map.TILE_SIZE,
                    )
                    tile = Tile(img_tile, rect_tile, tile["type"], tile["muro"])
                    if tile.wall:
                        self.visible_not_path.add(tile)
                    else:
                        self.visible_path.add(tile)
                for item in self.map.items.values():
                    item_tile_x = item.rect.x // Map.TILE_SIZE
                    item_tile_y = item.rect.y // Map.TILE_SIZE
                    if x == item_tile_x and y == item_tile_y:
                        self.visible_items.add(
                            Item(id, item, self.map.tiles_images[item["img"]])
                        )
                for monster in self.map.monsters.values():
                    monster_tile_x = monster.rect.x // Map.TILE_SIZE
                    monster_tile_y = monster.rect.y // Map.TILE_SIZE
                    if x == monster_tile_x and y == monster_tile_y:
                        monster_sprite = Monster(self.db, id)
                        monster_sprite.load(monster)
                        self.move_monster(monster)
                        self.visible_monsters.add(monster_sprite)

    # todo aggiustare:
    #   coordinate mappa vs coordinate assolute;
    #   coordinate topleft vs coordinate centro
    def move_monster(self, monster: Monster):
        shown = False
        last_target = None
        nop = 0
        path = []
        if (
            self.distance(monster.rect.center, self.player.rect.center)
            <= monster.raggio_vista
        ):
            if self.can_show(monster.rect.center, self.player.rect.center):
                shown = True
        if shown:
            now = pygame.time.get_ticks()
            if not path or last_target != self.player.rect.center or now - nop > 1000:
                path = self.bfs(monster.rect.center, self.player.rect.center)
                last_target = self.player.rect.center
                nop = now
        self.follow_path(monster, path)

    def distance(self, a: tuple, b: tuple):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def can_show(self, start: tuple, end: tuple):
        check = True
        for x, y in self.bresenham(start, end):
            if self.map.tiled_map[y][x]["muro"]:
                check = False
        return check

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

    def bfs(self, map: Map, start: tuple, end: tuple):
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

    def near_path(self, map: Map, pos: tuple):
        x, y = pos
        adiacenti = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [p for p in adiacenti if not map[p[1]][p[0]]["muro"]]

    def follow_path(self, monster: Monster, path: list):
        if path:
            next = self.path[0]
            if next != monster.rect.center:
                monster.rect.center = next
                path.pop(0)
