import pygame as pg
from settings import *


_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 4, _, _, _, 4, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Map:

    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()


    def get_map(self):
        for i, row in enumerate(self.mini_map):
            for j, value in enumerate(row):
                if value:
                    self.world_map[(j, i)] = value

    def draw(self):
        for (x, y), tile in self.world_map.items():
            pg.draw.rect(self.game.screen, 'darkgray', (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
