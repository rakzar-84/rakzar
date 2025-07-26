from typing import TYPE_CHECKING

import pygame

import gamestate.interface.interface as interface
import state
from core import GSprite

if TYPE_CHECKING:
    from map import Map


class Gameplay(interface.Interface):

    menu: "GSprite"
    party_info: "GSprite"
    mission_info: "GSprite"
    characters: "GSprite"
    gaming_area: "GSprite"
    minimap: "GSprite"
    dialog: "GSprite"

    def __init__(self):
        super().__init__()
        self.sprite_set = pygame.sprite.Group()
        self.menu = Menu(self.sprite_set, self.screen)
        self.party_info = PartyInfo(self.sprite_set, self.screen)
        self.mission_info = MissionInfo(self.sprite_set, self.screen)
        self.characters = Characters(self.sprite_set, self.screen)
        self.gaming_area = GamingArea(self.sprite_set, self.screen)
        self.minimap = Minimap(self.sprite_set, self.screen)
        self.dialog = Dialog(self.sprite_set, self.screen)


class Menu(GSprite):

    screen: interface.Screen

    def __init__(self, group: pygame.sprite.Group, screen: interface.Screen):
        super().__init__(group)
        self.screen = screen

    def init(self):
        w, h, x, y = self.calculate()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        area_w = self.screen.screen_info.current_w - state.config["interfaccia"]["cornice"] * 2
        w = area_w * state.config["interfaccia"]["left"]
        h = state.config["interfaccia"]["top"]
        x = state.config["interfaccia"]["cornice"]
        y = state.config["interfaccia"]["cornice"]
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        background = pygame.image.load("assets/button.png").convert_alpha()
        w_orig, h_orig = background.get_size()
        rapporto = w_orig / h_orig
        w_new = self.rect.w
        h_new = self.rect.w // rapporto
        if h_new > self.rect.h:
            h_new = self.rect.h
            w_new = h_new * rapporto
        background = pygame.transform.smoothscale(background, (w_new, h_new))
        x = (self.rect.w - w_new) // 2
        y = (self.rect.h - h_new) // 2
        self.image.blit(background, (x, y))


class PartyInfo(GSprite):

    screen: interface.Screen

    def __init__(self, group: pygame.sprite.Group, screen: interface.Screen):
        super().__init__(group)
        self.screen = screen

    def init(self):
        w, h, x, y = self.calculate()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        area_w = self.screen.screen_info.current_w - state.config["interfaccia"]["cornice"] * 2
        w = area_w * state.config["interfaccia"]["patyinfo"]
        h = state.config["interfaccia"]["top"]
        x = area_w * state.config["interfaccia"]["left"] + state.config["interfaccia"]["cornice"]
        y = state.config["interfaccia"]["cornice"]
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        surf_w, surf_h = self.image.get_size()
        interface.create_background("background2.png", self.image, surf_w, surf_h)


class MissionInfo(GSprite):

    screen: interface.Screen

    def __init__(self, group: pygame.sprite.Group, screen: interface.Screen):
        super().__init__(group)
        self.screen = screen

    def init(self):
        w, h, x, y = self.calculate()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        area_w = self.screen.screen_info.current_w - state.config["interfaccia"]["cornice"] * 2
        w = area_w * state.config["interfaccia"]["missione"]
        h = state.config["interfaccia"]["top"]
        left = state.config["interfaccia"]["left"] + state.config["interfaccia"]["patyinfo"]
        x = area_w * left + state.config["interfaccia"]["cornice"]
        y = state.config["interfaccia"]["cornice"]
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        surf_w, surf_h = self.image.get_size()
        interface.create_background("background2.png", self.image, surf_w, surf_h)


class Characters(GSprite):

    screen: interface.Screen

    def __init__(self, group: pygame.sprite.Group, screen: interface.Screen):
        super().__init__(group)
        self.screen = screen

    def init(self):
        w, h, x, y = self.calculate()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        area_w = self.screen.screen_info.current_w - state.config["interfaccia"]["cornice"] * 2
        area_h = self.screen.screen_info.current_h - state.config["interfaccia"]["cornice"] * 2
        w = area_w * state.config["interfaccia"]["left"]
        h = area_h - state.config["interfaccia"]["cornice"] - state.config["interfaccia"]["top"]
        x = state.config["interfaccia"]["cornice"]
        y = state.config["interfaccia"]["top"] + state.config["interfaccia"]["cornice"]
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 255))


class GamingArea(GSprite):

    screen: interface.Screen

    def __init__(self, group: pygame.sprite.Group, screen: interface.Screen):
        super().__init__(group)
        self.screen = screen

    def init(self):
        w, h, x, y = self.calculate()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        area_w = self.screen.screen_info.current_w - state.config["interfaccia"]["cornice"] * 2
        area_h = self.screen.screen_info.current_h - state.config["interfaccia"]["cornice"] * 2
        w = area_w * (1 - state.config["interfaccia"]["left"])
        h = area_h - state.config["interfaccia"]["top"]
        x = area_w * state.config["interfaccia"]["left"] + state.config["interfaccia"]["cornice"]
        y = state.config["interfaccia"]["top"] + state.config["interfaccia"]["cornice"]
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 0))


# todo il testo deve andare a capo
class Dialog(GSprite):

    screen: interface.Screen

    def __init__(self, group: pygame.sprite.Group, screen: interface.Screen):
        super().__init__(group)
        self.screen = screen
        self.text = ""

    def init(self):
        w, h, x, y = self.calculate()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        area_w = self.screen.screen_info.current_w - state.config["interfaccia"]["cornice"] * 2
        area_h = self.screen.screen_info.current_h - state.config["interfaccia"]["cornice"] * 2
        w = area_w * state.config["interfaccia"]["dialogw"]
        h = state.config["interfaccia"]["dialogh"]
        offset = state.config["interfaccia"]["left"] + (1 - state.config["interfaccia"]["left"] - state.config["interfaccia"]["dialogw"]) / 2
        x = area_w * offset + state.config["interfaccia"]["cornice"]
        y = area_h - state.config["interfaccia"]["dialogh"] + state.config["interfaccia"]["cornice"]
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, state.config["interfaccia"]["dialoga"]))
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), 3)
        y = 10
        font = pygame.font.SysFont(None, 24)
        for line in self.text.splitlines():
            text_surface = font.render(line, True, (255, 255, 255))
            self.image.blit(text_surface, (10, y))
            y += 30


class Minimap(GSprite):

    map: "Map"
    screen: interface.Screen

    def __init__(self, group: pygame.sprite.Group, screen: interface.Screen):
        super().__init__(group)
        self.screen = screen
        self.rect = None
        self.image = None
        self.map = None

    def init(self):
        w, h, x, y = self.calculate()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        area_w = self.screen.screen_info.current_w - state.config["interfaccia"]["cornice"] * 2
        w = area_w * state.config["interfaccia"]["minimap"]
        h = w // self.map.width * self.map.height
        x = area_w - w + state.config["interfaccia"]["cornice"]
        y = state.config["interfaccia"]["top"] + state.config["interfaccia"]["cornice"]
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, state.config["interfaccia"]["minimapa"]))
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), 3)
