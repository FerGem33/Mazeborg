from settings import *
from support import *
import json
from pytmx import load_pygame, TiledTileLayer
from tile import Tile
from camera import CameraGroup
from panel import Panel
from character import Character

from drag_and_drop import DragAndDrop


class Level(Panel):
    """
    The panel where the level is displayed.
    """
    def __init__(self):
        super().__init__((0, 0), (GAME_WIDTH, HEIGHT), pygame.display.get_surface(),(0, 0), '#FFFFFF')

        # Sprite groups
        self.ground = CameraGroup(self.surface)
        self.visible = CameraGroup(self.surface)
        self.collidable = pygame.sprite.Group()

        self.character = None
        self.script = None

        self.load('Calabozo')
        self.dragdrop = DragAndDrop(self.character)

    def restart(self):
        self.character.restart()
        self.dragdrop.script.executed = False

    def create_map(self, path):
        """
        Loads the map using pytmx.
        Parameters
        ----------
        path : the path to the tmx file that contains the data of the map
        """
        tmx_data = load_pygame(path)

        for layer in tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:  # Ensure the tile exists
                        tile = pygame.transform.scale(tile, (TILESIZE, TILESIZE))
                        pos = (x * TILESIZE, y * TILESIZE)

                        if layer.name == "ground":
                            Tile(pos, [self.ground], 'ground', tile)
                        elif layer.name == "walls":
                            Tile(pos, [self.visible, self.collidable], 'wall', tile)
                        elif layer.name == "items":
                            Tile(pos, [self.visible, self.collidable], 'item1', tile)
                        elif layer.name == "items2":
                            Tile(pos, [self.visible], 'item2', tile)

    def load(self, map_name: str):
        with open('map/index.json', 'r') as file:
            data = json.load(file)

        map_data = None
        for level in data['levels']:
            if map_name == level['name']:
                map_data = level

        self.fill_color = map_data['bg_color']

        spawn = (map_data['spawn']['x'] * TILESIZE, map_data['spawn']['y'] * TILESIZE)
        self.character = Character(spawn, [self.visible], self.collidable)

        self.create_map(map_data['path'])

    def run(self, event_list):
        self.surface.fill(self.fill_color)
        self.ground.draw(self.character, event_list)
        self.visible.draw(self.character, event_list)
        self.draw_surface.blit(self.surface, self.rect)
        # self.ground.update()
        self.visible.update()

        if self.dragdrop.run(event_list):
            self.restart()
        if self.dragdrop.script.executing:
            self.ground.centered_view = True
            self.visible.centered_view = True
