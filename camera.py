from core import GSprite
from map import Map


class Camera:

    target: GSprite
    scene: GSprite
    width: int
    height: int
    map_w: int
    map_h: int
    x: int
    y: int

    def __init__(self, target: GSprite, scene: GSprite, map: Map):
        self.target = target
        self.scene = scene
        self.width = scene.rect.width
        self.height = scene.rect.height
        self.map_w = map.width
        self.map_h = map.height
        self.x = 0
        self.y = 0

    def update(self, resize: bool):
        if resize:
            self.width = self.scene.rect.width
            self.height = self.scene.rect.height
        self.x = max(self.width // 2, self.target.rect.centerx)
        self.y = max(self.height // 2, self.target.rect.centery)
        self.x = min(self.x, self.map_w - self.width // 2)
        self.y = min(self.y, self.map_h - self.height // 2)
