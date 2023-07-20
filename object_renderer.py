import pygame as pg
from settings import *

class ObjectRenderer:

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()


    def draw(self):
        self.render_game_objects()


    def render_game_objects(self):
        for depth, image, pos in self.game.raycasting.objects_to_render:
            self.screen.blit(image, pos)


    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)


    def load_wall_textures(self):
        return {n: self.get_texture(f'resources/textures/{n}.png') for n in range(1, 6)}
