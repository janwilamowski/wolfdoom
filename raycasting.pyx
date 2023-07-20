# cython: profile=True
import cython
from libc.math cimport sin
from libc.math cimport cos
import pygame as pg
from settings import *

cdef class RayCasting:

    cdef public list objects_to_render
    cdef object game
    cdef list raycasting_result
    cdef dict textures

    def __init__(self, game):
        self.game = game
        self.objects_to_render = []
        self.raycasting_result = []
        self.textures = game.object_renderer.wall_textures


    cdef void get_objects_to_render(RayCasting self):
        self.objects_to_render = []
        cdef:
            int ray = 0
            int scale = SCALE
            int texture_size = TEXTURE_SIZE
            int half_texture_size = HALF_TEXTURE_SIZE
            int height = HEIGHT
            int half_height = HALF_HEIGHT
            int texture
            int zero = 0
            int one = 1
            int two = 2
            double depth, proj_height, offset, texture_height
            object wall_column
            tuple wall_pos, scale_params, result

        for values in self.raycasting_result:
            depth, proj_height, texture, offset = values
            if proj_height < height:
                wall_column = self.textures[texture].subsurface(
                    offset * (texture_size - scale), zero, scale, texture_size
                )
                scale_params = (scale, proj_height)
                wall_pos = (ray * scale, half_height - proj_height // two)
            else:
                texture_height = texture_size * height / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (texture_size - scale), half_texture_size - texture_height / two,
                    scale,texture_height
                )
                scale_params = (scale, height)
                wall_pos = (ray * scale, zero)

            wall_column = pg.transform.scale(wall_column, scale_params)
            result = (depth, wall_column, wall_pos)
            self.objects_to_render.append(result)
            ray += one


    # def raycast(self):
    cdef void raycast(RayCasting self, double ox, double oy, double x_map, double y_map, double player_angle):
        cdef int nrays, ray, max_depth, tile_size, scale, screen_dist, half_height, two, three
        cdef double ray_angle, sin_a, cos_a, dx, dy, delta_angle, half_fov#, ox, oy
        cdef double y_hor, x_hor, x_vert, y_vert, offset#, x_map, y_map, player_angle
        cdef double delta_depth, depth_hor, depth_vert, depth, proj_height
        cdef double one, zero, minus_one, millionth, eps
        cdef tuple tile_hor, tile_vert, result, line_start, line_end
        cdef object texture, texture_vert, texture_hor

        nrays = NUM_RAYS
        max_depth = MAX_DEPTH
        tile_size = TILE_SIZE
        scale = SCALE
        screen_dist = SCREEN_DIST
        half_height = HALF_HEIGHT
        delta_angle = DELTA_ANGLE
        half_fov = HALF_FOV
        # player_angle = self.game.player.angle
        minus_one = -1
        zero = 0
        one = 1
        two = 2
        three = 3
        eps = 0.0001
        millionth = 1e-6

        # ox, oy = self.game.player.pos
        # x_map, y_map = self.game.player.map_pos

        self.raycasting_result.clear()
        ray_angle = player_angle - half_fov + eps
        for ray in range(nrays):
            sin_a = sin(ray_angle)
            cos_a = cos(ray_angle)

            # horizontals
            if sin_a > zero:
                y_hor = y_map + one
                dy = one
            else:
                y_hor = y_map - millionth
                dy =  minus_one
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(max_depth):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            if cos_a > zero:
                x_vert = x_map + one
                dx = one
            else:
                x_vert = x_map - millionth
                dx = minus_one
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(max_depth):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= one
                offset = y_vert if cos_a > zero else one - y_vert
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= one
                offset = x_hor if sin_a > zero else one - x_hor

            # remove fishbowl effect
            depth *= cos(player_angle - ray_angle)

            if self.game.show_map:
                # 2D debug
                line_start = (ox * tile_size, oy * tile_size)
                line_end = ((ox + depth*cos_a) * tile_size, (oy + depth*sin_a) * tile_size)
                pg.draw.line(self.game.screen, 'yellow', line_start, line_end)
            else:
                # projection
                proj_height = screen_dist / (depth + eps)
                # wall_color = [255 / (one + depth ** 5 * 0.00002)] * three
                # pg.draw.rect(self.game.screen, wall_color,
                #     (ray * scale, half_height - proj_height // two, scale, proj_height), 1)
                result = (depth, proj_height, texture, offset)
                self.raycasting_result.append(result)

            ray_angle += delta_angle


    def update(self):
        cdef RayCasting this = self
        pos = self.game.player.pos
        map_pos = self.game.player.map_pos
        this.raycast(pos[0], pos[1], map_pos[0], map_pos[1], self.game.player.angle)
        this.get_objects_to_render()


    def draw(self):
        pass
