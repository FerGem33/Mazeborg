import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    """
    The tiles that represent textures in the map.
    """
    def __init__(self, pos, groups, tile_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        """
        Parameters
        ----------
        pos : tuple
        The relative position of the tile to its draw surface
        groups : list
        The groups that the tile belongs to
        tile_type : str
        The type of tile to draw
        surface : pygame.Surface
        The surface or image of the tile, defaults to a black surface
        """
        super().__init__(*groups)
        self.tile_type = tile_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)

        if self.tile_type == 'object':
            self.hitbox = self.rect.inflate(0, -74)
        else:
            self.hitbox = self.rect.inflate(0, -10)
