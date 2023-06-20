import cython
from libc.math cimport sin
from libc.math cimport cos
import pygame as pg
from settings import *

class RayCasting:

    def __init__(self, game):
        self.game = game


    def raycast(self):
        cdef int nrays, ray, max_depth, tile_size, scale, screen_dist, half_height, two, three
        cdef double ox, oy, ray_angle, sin_a, cos_a, dx, dy, delta_angle, half_fov
        cdef double y_hor, x_hor, x_vert, y_vert, x_map, y_map, player_angle
        cdef double delta_depth, depth_hor, depth_vert, depth, proj_height
        cdef double one, zero, minus_one, millionth, eps
        cdef tuple tile_hor, tile_vert

        nrays = NUM_RAYS
        max_depth = MAX_DEPTH
        tile_size = TILE_SIZE
        scale = SCALE
        screen_dist = SCREEN_DIST
        half_height = HALF_HEIGHT
        delta_angle = DELTA_ANGLE
        half_fov = HALF_FOV
        player_angle = self.game.player.angle
        minus_one = -1
        zero = 0
        one = 1
        two = 2
        three = 3
        eps = 0.0001
        millionth = 1e-6

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = player_angle - half_fov + eps
        for ray in range(nrays):
            sin_a = sin(ray_angle)
            cos_a = cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map+one, one) if sin_a > zero else (y_map-millionth, minus_one)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(max_depth):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map+one, one) if cos_a > zero else (x_map-millionth, minus_one)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(max_depth):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            depth = min(depth_hor, depth_vert)

            # remove fishbowl effect
            depth *= cos(player_angle - ray_angle)

            if self.game.show_map:
                # 2D debug
                pg.draw.line(self.game.screen, 'yellow', (ox*tile_size, oy*tile_size),
                        ((ox + depth*cos_a) * tile_size, (oy + depth*sin_a) * tile_size))
            else:
                # projection
                proj_height = screen_dist / (depth + eps)
                wall_color = [255 / (one + depth ** 5 * 0.00002)] * three
                pg.draw.rect(self.game.screen, wall_color,
                    (ray * scale, half_height - proj_height // two, scale, proj_height), 1)

            ray_angle += delta_angle


    def update(self):
        self.raycast()


    def draw(self):
        pass
