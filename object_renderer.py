import pygame as pg
from settings import *

class ObjectRenderer:

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()


    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)


    def load_wall_textures(self):
        return {n: self.get_texture(f'resources/textures/{n}.png') for n in range(1, 6)}
