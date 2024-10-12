from settings import *
from support import *
from random import choice
from robot import Robot
from tile import Tile
from camera import CameraGroup
from panel import Panel


class Game(Panel):
    """
    The panel where the game is displayed.
    """
    def __init__(self):
        super().__init__((0, 0), (GAME_WIDTH, HEIGHT), pygame.display.get_surface(),(0, 0), 'cadetblue2')

        # Sprite groups
        self.visible_sprites = CameraGroup(self.surface)
        self.collidable_sprites = pygame.sprite.Group()

        self.robot = None
        self.create_map()

    def create_map(self):
        """
        Generates the map and loads textures according to layouts provided in CSV files.
        """
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
        self.surface.fill(self.fill_color)
        self.visible_sprites.draw(self.robot)
        self.draw_surface.blit(self.surface, self.rect)
        self.visible_sprites.update()
