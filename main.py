import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import pygame as pg
from map import Map
from object_renderer import ObjectRenderer
from player import Player
from raycasting import RayCasting
# from raycasting_vanilla import RayCasting
from settings import *


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.dt = 1
        self.map = Map(self)
        self.player = Player(self, PLAYER_POS)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.show_map = False


    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


    def update(self):
        # keys = pg.key.get_pressed()
        # if keys[pg.K_m]:

        self.player.update()
        self.raycasting.update()
        pg.display.flip()
        self.dt = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')


    def draw(self):
        self.screen.fill('black')
        if self.show_map:
            self.map.draw()
            self.player.draw()
        self.raycasting.draw()
        self.object_renderer.draw()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()

                pr.disable()
                s = io.StringIO()
                sortby = 'tottime' #'cumulative' #SortKey.CUMULATIVE
                with open('stats.log', 'w') as s:
                    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                    ps.print_stats()

                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.show_map = not self.show_map


if __name__ == '__main__':
    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()

    game = Game()
    game.run()

