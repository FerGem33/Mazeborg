import pygame
from settings import *
from codeblock import CodeBlock
from panel import Panel, BlockPanel


class DragAndDrop(Panel):
    def __init__(self):
        pos = (GAME_WIDTH, 0)
        super().__init__(pos, (DRAG_WIDTH + DROP_WIDTH, HEIGHT), pygame.display.get_surface(), pos)
        pos = (DROP_WIDTH, 0)
        self.drag = BlockPanel(pos, 'drag', self.surface, self.offset + pos)
        pos = (0, 0)
        self.drop = BlockPanel(pos, 'drop', self.surface, self.offset + pos)

        # Blocks
        self.drag.add_block((DROP_WIDTH + 30, 30))
        self.drop.add_block((30, 30))

    def run(self, event_list):
        # Draw the drag and drop panels
        self.drag.draw()
        self.drop.draw()

        # Update the blocks
        self.drag.update(event_list)
        self.drop.update(event_list)

        # Draw the blocks onto the panel
        for block in self.drag.blocks:
            block.draw()
        for block in self.drop.blocks:
            block.draw()

        # Draw the panel on the screen
        self.draw_surface.blit(self.surface, self.rect)
