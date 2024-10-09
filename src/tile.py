import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(*groups)
        self.tile_type = tile_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)

        if self.tile_type == 'object':
            self.hitbox = self.rect.inflate(0, -74)
        else:
            self.hitbox = self.rect.inflate(0, -10)
