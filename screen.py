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
        background = pygame.image.load("assets/background.png").convert_alpha()
        tile_w, tile_h = background.get_size()
        surf_w, surf_h = self.image.get_size()
        for y in range(0, surf_h, tile_h):
            for x in range(0, surf_w, tile_w):
                self.image.blit(background, (x, y))
        x = 0
        top = pygame.image.load("assets/frame_t.png").convert_alpha()
        t_w, t_h = top.get_size()
        while x < surf_w:
            self.image.blit(top, (x, 0))
            x += t_w
        x = 0
        bottom = pygame.image.load("assets/frame_b.png").convert_alpha()
        b_w, b_h = bottom.get_size()
        while x < surf_w:
            self.image.blit(bottom, (x, surf_h - b_h))
            x += b_w
        y = 0
        left = pygame.image.load("assets/frame_l.png").convert_alpha()
        l_w, l_h = left.get_size()
        while y < surf_h:
            self.image.blit(left, (0, y))
            y += l_h
        y = 0
        right = pygame.image.load("assets/frame_r.png").convert_alpha()
        r_w, r_h = right.get_size()
        while y < surf_h:
            self.image.blit(right, (surf_w - r_w, y))
            y += l_h
        tl = pygame.image.load("assets/frame_tl.png").convert_alpha()
        self.image.blit(tl, (0, 0))
        tr = pygame.image.load("assets/frame_tr.png").convert_alpha()
        tr_w, tr_h = tr.get_size()
        self.image.blit(tr, (surf_w - tr_w, 0))
        bl = pygame.image.load("assets/frame_bl.png").convert_alpha()
        bl_w, bl_h = bl.get_size()
        self.image.blit(bl, (0, surf_h - bl_h))
        br = pygame.image.load("assets/frame_br.png").convert_alpha()
        br_w, br_h = br.get_size()
        self.image.blit(br, (surf_w - br_w, surf_h - br_h))
