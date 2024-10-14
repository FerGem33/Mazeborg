import pygame
from settings import *
from codeblock import CodeBlock


class Panel:
    """
    This serves as an abstract class to panels, the different sections the game screen is split into.
    """
    def __init__(self, pos, size, draw_surface, offset=(0, 0), fill_color=(0, 0, 0)):
        """
        Parameters
        ----------
        pos : tuple
        The relative position of the panel to its draw surface.
        size : tuple
        The width and height of the panel in pixels.
        draw_surface : pygame.Surface
        The surface to draw the panel on.
        offset : tuple
        The distance in x and y from (0,0) of pygame's display.
        fill_color : pygame.color | str
        The fill color of the panel.
        """
        self.draw_surface = draw_surface
        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(topleft=pos)
        self.offset = offset
        self.fill_color = fill_color

    def abs_rect(self) -> pygame.rect.Rect:
        """Returns the absolute rect respect to the pygame display."""
        rect = self.rect.copy()
        rect.x += self.offset[0]
        rect.y += self.offset[1]
        return rect

    def draw(self):
        """
        Draws the panel on its draw surface
        """
        self.surface.fill(self.fill_color)
        self.draw_surface.blit(self.surface, self.rect)

    def run(self):
        """
        The method executed on each iteration of the main game loop.
        """
        pass


class BlockPanel(Panel):
    """
    A panel that contains CodeBlocks and allows its manipulation.
    """
    def __init__(self, pos, panel_type, draw_surface, offset):
        """
        Parameters
        ----------
        pos : tuple
        The relative position of the panel to its draw surface.
        panel_type : str
        The type of panel to create. Possible values: 'drag', 'drop'.
        draw_surface : pygame.Surface
        The surface to draw the panel on.
        """
        width = None
        fill_color = None
        blocks_color = None

        if panel_type == 'drag':
            width = DRAG_WIDTH
            fill_color = 'snow4'
            blocks_color = 'crimson'
        elif panel_type == 'drop':
            width = DROP_WIDTH
            fill_color = 'slategray3'
            blocks_color = 'mediumslateblue'

        super().__init__(pos, (width, HEIGHT), draw_surface, offset, fill_color)
        self.blocks_color = blocks_color
        self.blocks = pygame.sprite.Group()

    def add_block(self, pos):
        """
        Adds a block to the panel.
        Parameters
        ----------
        pos : tuple
        The relative position of the panel to its draw surface.
        """
        block = CodeBlock(pos, self, self.draw_surface, self.blocks_color)
        self.blocks.add(block)

    def update(self, event_list) -> list:
        """
        Updates all blocks in the panel and returns a list of the blocks that were moved out from it.
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """
        blocks = []
        for block in self.blocks:
            if block.update(event_list):
                blocks.append(block)
        return blocks
