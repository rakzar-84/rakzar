import pygame

import state


class Screen:

    image: pygame.Surface
    screen_info: pygame.display.Info

    def __init__(self):
        self.image = None
        self.screen_info = None

    def init(self):
        self.screen_info = pygame.display.Info()
        pygame.display.set_caption(state.config["nome"] + " - v. " + state.config["versione"])
        if state.config["fullscreen"]:
            self.to_fullscreen()
        else:
            self.to_window()

    def to_window(self):
        if self.image is not None and bool(self.image.get_flags() & pygame.FULLSCREEN):
            # debug reimpostare
            # w = self.screen_info.current_w - 100
            # h = self.screen_info.current_h - 100
            # self.image = pygame.display.set_mode((w, h), pygame.RESIZABLE)
            self.image = pygame.display.set_mode((1366, 768), pygame.RESIZABLE)

    def to_fullscreen(self):
        if self.image is None or not bool(self.image.get_flags() & pygame.FULLSCREEN):
            self.image = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def update(self):
        if state.resize:
            self.screen_info = pygame.display.Info()

    def draw(self):
        self.image.fill((0, 0, 0))
        surf_w, surf_h = self.image.get_size()
        create_background("background.png", self.image, surf_w, surf_h)
        create_frame("frame.png", self.image, surf_w, surf_h)


class Interface:

    screen: Screen
    sprite_set: pygame.sprite.Group

    def __init__(self):
        self.screen = Screen()

    def init(self):
        self.screen.init()
        if state.resize:
            for sprite in self.sprite_set:
                sprite.init()

    def to_window(self):
        self.screen.to_window()

    def to_fullscreen(self):
        self.screen.to_fullscreen()

    def update(self):
        self.screen.update()

    def draw(self):
        self.screen.draw()
        for sprite in self.sprite_set:
            sprite.draw()

    def render(self):
        self.sprite_set.draw(self.screen.image)


def create_background(name: str, image: pygame.Surface, surf_w: int, surf_h: int):
    background = pygame.image.load("assets/" + name).convert_alpha()
    tile_w, tile_h = background.get_size()
    for y in range(0, surf_h, tile_h):
        for x in range(0, surf_w, tile_w):
            image.blit(background, (x, y))


def create_frame(name: str, image: pygame.Surface, surf_w: int, surf_h: int):
    x = 0
    top = pygame.image.load("assets/t_" + name).convert_alpha()
    t_w, t_h = top.get_size()
    while x < surf_w:
        image.blit(top, (x, 0))
        x += t_w
    x = 0
    bottom = pygame.image.load("assets/b_" + name).convert_alpha()
    b_w, b_h = bottom.get_size()
    while x < surf_w:
        image.blit(bottom, (x, surf_h - b_h))
        x += b_w
    y = 0
    left = pygame.image.load("assets/l_" + name).convert_alpha()
    l_w, l_h = left.get_size()
    while y < surf_h:
        image.blit(left, (0, y))
        y += l_h
    y = 0
    right = pygame.image.load("assets/r_" + name).convert_alpha()
    r_w, r_h = right.get_size()
    while y < surf_h:
        image.blit(right, (surf_w - r_w, y))
        y += l_h
    tl = pygame.image.load("assets/tl_" + name).convert_alpha()
    image.blit(tl, (0, 0))
    tr = pygame.image.load("assets/tr_" + name).convert_alpha()
    tr_w, tr_h = tr.get_size()
    image.blit(tr, (surf_w - tr_w, 0))
    bl = pygame.image.load("assets/bl_" + name).convert_alpha()
    bl_w, bl_h = bl.get_size()
    image.blit(bl, (0, surf_h - bl_h))
    br = pygame.image.load("assets/br_" + name).convert_alpha()
    br_w, br_h = br.get_size()
    image.blit(br, (surf_w - br_w, surf_h - br_h))
