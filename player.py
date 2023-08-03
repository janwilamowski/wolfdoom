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
        keys = pg.key.get_pressed()

        speed = PLAYER_SPEED * self.game.dt
        if keys[pg.K_LSHIFT]:
            speed *= 2

        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

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

        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.dt
        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.dt
        self.angle %= math.tau


    def check_wall(self, x, y):
        return (int(x), int(y)) not in self.game.map.world_map


    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.dt
        if self.check_wall(self.x + dx * scale, self.y):
            self.x += dx
        if self.check_wall(self.x, self.y + dy * scale):
            self.y += dy


    def update(self):
        self.move()
        self.mouse_control()


    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.dt


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
