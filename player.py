import math
import pygame as pg
from settings import *

class Player:

    def __init__(self, game, pos):
        self.game = game
        self.x, self.y = pos
        self.angle = PLAYER_ANGLE


    def move(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.dt
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos

        # self.x += dx
        # self.y += dy
        self.check_wall_collision(dx, dy)

        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.dt
        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.dt
        self.angle %= math.tau


    def check_wall(self, x, y):
        return (int(x), int(y)) not in self.game.map.world_map


    def check_wall_collision(self, dx, dy):
        if self.check_wall(self.x + dx, self.y):
            self.x += dx
        if self.check_wall(self.x, self.y + dy):
            self.y += dy


    def update(self):
        self.move()


    @property
    def pos(self):
        return self.x, self.y


    @property
    def pos_world(self):
        return self.x*TILE_SIZE, self.y*TILE_SIZE


    @property
    def map_pos(self):
        return int(self.x), int(self.y)


    def draw(self):
        pg.draw.circle(self.game.screen, 'green', self.pos_world, 10)
        pg.draw.line(self.game.screen, 'green', self.pos_world,
                (self.pos_world[0] + math.cos(self.angle)*50,
                 self.pos_world[1] + math.sin(self.angle)*50))
