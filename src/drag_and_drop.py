import pygame
from settings import *
from functools import partial
from panel import Panel, BlockPanel
from character import Character
from script import Script


class DragAndDrop(Panel):
    """
    The panel that contains the blocks of code and manages the drag and drop interface.
    """
    def __init__(self, character):
        """
        Parameters
        ----------
        character : Character
        The character that the blocks of code control.
        """
        pos = (GAME_WIDTH, 0)
        super().__init__(pos, (DRAG_WIDTH + DROP_WIDTH, HEIGHT), pygame.display.get_surface(), pos)
        pos = (DROP_WIDTH, 0)
        self.drag = BlockPanel(pos, 'drag', self.surface, self.offset + pos)
        pos = (0, 0)
        self.drop = BlockPanel(pos, 'drop', self.surface, self.offset + pos)

        # Drag and Drop panels
        self.drag.add_block((DROP_WIDTH + 30, 30))
        self.drop.add_block((30, 30))
        self.character = character
        self.script = Script(self.character)
        script = [
            partial(self.character.move, 12),
            partial(self.character.rotate, -90),
            partial(self.character.move, 3),
            partial(self.character.rotate, -90),
            partial(self.character.move, 4),
            partial(self.character.rotate, 90),
            partial(self.character.move, 25),
            partial(self.character.rotate, 90),
            partial(self.character.move, 7),
            partial(self.character.rotate, -90),
            partial(self.character.move, 8),
            partial(self.character.rotate, 90),
            partial(self.character.move, 6),
            partial(self.character.rotate, 90),
            partial(self.character.move, 14),
            partial(self.character.rotate, -90),
            partial(self.character.move, 3),
            partial(self.character.rotate, -90),
            partial(self.character.move, 19),
            partial(self.character.rotate, -90),
            partial(self.character.move, 25),
            partial(self.character.rotate, -90),
            partial(self.character.move, 5),
            partial(self.character.rotate, -90),
            partial(self.character.move, 1),
        ]
        self.script.set_script(script)

    def to_drag(self, blocks):
        """
        Adds the given blocks to the Drag panel.
        Parameters
        ----------
        blocks : list
        The blocks to add to the Drag panel.
        """
        for block in blocks:
            self.drop.blocks.remove(block)
            # check if the block was not moved to the game panel
            """if block.abs_rect().x >= GAME_WIDTH:
                self.drag.add_block(block.rect.topleft)"""

    def to_drop(self, blocks):
        """
        Adds the given blocks to the Drop panel.
        Parameters
        ----------
        blocks : list
        The blocks to add to the Drop panel.
        """
        for block in blocks:
            self.drag.blocks.remove(block)
            # check if the block was not moved to the game panel
            if block.abs_rect().x >= GAME_WIDTH:
                self.drop.add_block(block.rect.topleft)

    def run(self, event_list):
        """
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """
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
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    self.script.start()
        self.script.update()
