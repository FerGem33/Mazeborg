import pygame
from settings import *
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

    def to_drag(self, blocks):
        for block in blocks:
            self.drop.blocks.remove(block)
            self.drag.add_block(block.rect.topleft)

    def to_drop(self, blocks):
        for block in blocks:
            self.drag.blocks.remove(block)
            self.drop.add_block(block.rect.topleft)

    def run(self, event_list):
        # Draw the drag and drop panels
        self.drag.draw()
        self.drop.draw()

        # Update the blocks
        from_drag = self.drag.update(event_list)
        from_drop = self.drop.update(event_list)
        self.to_drag(from_drop)
        self.to_drop(from_drag)

        # Draw the blocks onto the panel
        for block in self.drag.blocks:
            block.draw()
        for block in self.drop.blocks:
            block.draw()

        # Draw the panel on the screen
        self.draw_surface.blit(self.surface, self.rect)
