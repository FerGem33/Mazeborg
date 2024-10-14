from settings import *
from support import *
from random import choice
from tile import Tile
from camera import CameraGroup
from panel import Panel
from character import Character


class Game(Panel):
    """
    The panel where the game is displayed.
    """
    def __init__(self):
        super().__init__((0, 0), (GAME_WIDTH, HEIGHT), pygame.display.get_surface(),(0, 0), 'cadetblue2')

        # Sprite groups
        self.visible = CameraGroup(self.surface)
        self.collidable = pygame.sprite.Group()

        self.robot = None
        self.character = None
        self.script = None
        self.create_map()

        # self.robot = Robot((100, 250), [self.visible_sprites], self.collidable_sprites)
        self.character = Character((100, 200), [self.visible], self.collidable)

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

                        if style == 'wall':
                            Tile((x, y), [self.visible, self.collidable], 'wall', graphs['wall'][0])
                        if style == 'flower':
                            surf = choice(graphs['flower'])
                            Tile((x, y), [self.visible], 'object', surf)

    def run(self):
        self.surface.fill(self.fill_color)
        self.visible.draw(self.character)
        self.draw_surface.blit(self.surface, self.rect)
        self.visible.update()
