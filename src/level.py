import pygame
from support import *
from settings import *
from random import choice
from robot import Robot
from tile import Tile


class Level:
    def __init__(self):
        self.display = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = CameraGroup()
        self.collidable_sprites = pygame.sprite.Group()

        # Map
        self.create_map()

    def create_map(self):
        layouts = {
            'ground': import_csv_layout('map/ground.csv'),
            'wall': import_csv_layout('map/walls.csv'),
            'flower': import_csv_layout('map/obj.csv'),
        }
        graphs = {
            'ground': import_folder('assets/images/grass'),
            'wall': import_folder('assets/images/stone'),
            'flower': import_folder('assets/images/flower'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column != '-1':
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE

                        """if style == 'ground':
                            surf = choice(graphs['ground'])
                            Tile((x, y), [self.visible_sprites], 'ground', surf)"""
                        if style == 'wall':
                            Tile((x, y), [self.visible_sprites, self.collidable_sprites], 'wall', graphs['wall'][0])
                        if style == 'flower':
                            surf = choice(graphs['flower'])
                            Tile((x, y), [self.visible_sprites], 'object', surf)

        self.robot = Robot((100, 250), [self.visible_sprites], self.collidable_sprites)

    def run(self):
        self.visible_sprites.draw(self.robot)
        self.visible_sprites.update()
        # self.iu.display(self.robot)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.ground_surf = pygame.image.load('assets/images/ground.png').convert()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def draw(self, robot):
        self.offset.x = robot.rect.centerx - self.half_width
        self.offset.y = robot.rect.centery - self.half_height

        ground_pos = self.ground_rect.topleft - self.offset
        self.display.blit(self.ground_surf, ground_pos)

        for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
            new_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, new_pos)
