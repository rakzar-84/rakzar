import pygame

from core import GSprite
from screen import Screen


class Interface:

    screen: Screen
    sprite_set: pygame.sprite.Group
    menu: GSprite
    party_info: GSprite
    mission_info: GSprite
    characters: GSprite
    gaming_area: GSprite
    minimap: GSprite
    dialog: GSprite

    def __init__(self, screen: Screen):
        self.screen = screen
        self.sprite_set = pygame.sprite.Group()
        self.menu = Menu(self.sprite_set, self.screen)
        self.party_info = PartyInfo(self.sprite_set, self.screen)
        self.mission_info = MissionInfo(self.sprite_set, self.screen)
        self.characters = Characters(self.sprite_set, self.screen)
        self.gaming_area = GamingArea(self.sprite_set, self.screen)
        self.minimap = Minimap(self.sprite_set, self.screen)
        self.dialog = Dialog(self.sprite_set, self.screen)

    def update(self, resize: bool):
        for sprite in self.sprite_set:
            sprite.update(resize)

    def draw(self):
        for sprite in self.sprite_set:
            sprite.draw()


# todo parametrizzare dimensioni interfaccia


class Menu(GSprite):

    screen: Screen

    def __init__(self, group: pygame.sprite.Group, screen: Screen):
        super().__init__(group)
        self.screen = screen

    def update(self, resize: bool):
        if resize:
            w, h, x, y = self.calculate()
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        w = (self.screen.screen_info.current_w - 20) // 5
        h = 80
        x = 10
        y = 10
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

    screen: Screen

    def __init__(self, group: pygame.sprite.Group, screen: Screen):
        super().__init__(group)
        self.screen = screen

    def update(self, resize: bool):
        if resize:
            w, h, x, y = self.calculate()
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        w = (self.screen.screen_info.current_w - 20) // 5 * 2
        h = 80
        x = (self.screen.screen_info.current_w - 20) // 5 + 10
        y = 10
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        background = pygame.image.load("assets/background2.png").convert_alpha()
        tile_w, tile_h = background.get_size()
        surf_w, surf_h = self.image.get_size()
        for y in range(0, surf_h, tile_h):
            for x in range(0, surf_w, tile_w):
                self.image.blit(background, (x, y))


class MissionInfo(GSprite):

    screen: Screen

    def __init__(self, group: pygame.sprite.Group, screen: Screen):
        super().__init__(group)
        self.screen = screen

    def update(self, resize: bool):
        if resize:
            w, h, x, y = self.calculate()
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        w = (self.screen.screen_info.current_w - 20) // 5 * 2
        h = 80
        x = (self.screen.screen_info.current_w - 20) // 5 * 3 + 10
        y = 10
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        background = pygame.image.load("assets/background2.png").convert_alpha()
        tile_w, tile_h = background.get_size()
        surf_w, surf_h = self.image.get_size()
        for y in range(0, surf_h, tile_h):
            for x in range(0, surf_w, tile_w):
                self.image.blit(background, (x, y))


class Characters(GSprite):

    screen: Screen

    def __init__(self, group: pygame.sprite.Group, screen: Screen):
        super().__init__(group)
        self.screen = screen

    def update(self, resize: bool):
        if resize:
            w, h, x, y = self.calculate()
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        w = (self.screen.screen_info.current_w - 20) // 5
        h = (self.screen.screen_info.current_h - 20) - 90
        x = 10
        y = 80
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 0))


class GamingArea(GSprite):

    screen: Screen

    def __init__(self, group: pygame.sprite.Group, screen: Screen):
        super().__init__(group)
        self.screen = screen

    def update(self, resize: bool):
        if resize:
            w, h, x, y = self.calculate()
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        w = (self.screen.screen_info.current_w - 20) // 5 * 4
        h = (self.screen.screen_info.current_h - 20) - 80
        x = (self.screen.screen_info.current_w - 20) // 5 + 10
        y = 90
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 0))


# todo il testo deve andare a capo
class Dialog(GSprite):

    screen: Screen

    def __init__(self, group: pygame.sprite.Group, screen: Screen):
        super().__init__(group)
        self.screen = screen
        self.text = ""

    def update(self, resize: bool):
        if resize:
            w, h, x, y = self.calculate()
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        w = (self.screen.screen_info.current_w - 20) // 2
        h = 150
        x = (self.screen.screen_info.current_w - 20) // 20 * 7 + 10
        y = (self.screen.screen_info.current_h - 20) - 150 + 10
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 200))
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), 3)
        y = 10
        font = pygame.font.SysFont(None, 24)
        for line in self.text.splitlines():
            text_surface = font.render(line, True, (255, 255, 255))
            self.image.blit(text_surface, (10, y))
            y += 30


class Minimap(GSprite):

    def __init__(self, group: pygame.sprite.Group, screen: Screen):
        super().__init__(group)
        self.screen = screen
        self.rect = None
        self.image = None

    def update(self, resize: bool):
        if resize:
            w, h, x, y = self.calculate()
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def calculate(self) -> tuple[int, int, int, int]:
        w = (self.screen.screen_info.current_w - 20) // 6
        h = w // 4 * 3  # todo le mappe non possono avere tutte queste proporzioni
        x = (self.screen.screen_info.current_w - 20) - w + 10
        y = 90
        return w, h, x, y

    def draw(self):
        self.image.fill((0, 0, 0, 100))
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), 3)
