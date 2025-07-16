import pygame

from map import Map


class Camera:

    def __init__(self, target:pygame.sprite.Sprite, area:pygame.sprite.Sprite, mappa:Map):
        self.target = target
        self.area = area
        self.mappa = mappa
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0

    def update(self):
        self.width = self.area.rect.width
        self.height = self.area.rect.height
        self.x = max(self.width//2, self.target.rect.centerx)
        self.y = max(self.height//2, self.target.rect.centery)
        self.x = min(self.x, self.mappa.width-self.width//2)
        self.y = min(self.y, self.mappa.height-self.height//2)
