from settings import *
from functools import partial
from panel import Panel, BlockPanel
from character import Character
from script import Script
from codeblock import InputBlock


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
        self.character = character
        pos = (GAME_WIDTH, 0)
        super().__init__(pos, (DRAG_WIDTH + DROP_WIDTH, HEIGHT), pygame.display.get_surface(), pos)
        pos = (DROP_WIDTH, 0)
        self.drag = BlockPanel(pos, 'drag', self.surface, self.offset + pos, self.character)
        pos = (0, 0)
        self.drop = BlockPanel(pos, 'drop', self.surface, self.offset + pos, self.character)

        # Drag and Drop panels
        types = ['movex', 'rotatex', 'smart_move', 'turn_right', 'turn_left', 'turn_back']
        for i, t in enumerate(types):
            for x in range(20):
                self.drag.add_block((DROP_WIDTH + 30, 15 + 70 * i), t)
        self.script = Script(self.character)

    def to_drag(self, blocks, destroy=False):
        """
        Adds the given blocks to the Drag panel.
        Parameters
        ----------
        blocks : list
        The blocks to add to the Drag panel.
        """
        if not destroy:
            for block in blocks:
                self.drop.blocks.remove(block)
                # check if the block was not moved to the game panel
                if block.abs_rect().x >= GAME_WIDTH:
                    self.drag.add_block(block.rect.topleft, block.block_type)
        else:
            for block in blocks:
                self.drop.blocks.remove(block)

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
                self.drop.add_block(block.rect.topleft, block.block_type)

    def update_script(self):
        script = [partial(self.character.rotate, 0)]
        for block in sorted(self.drop.blocks, key=lambda spr: spr.rect.top):
            if isinstance(block, InputBlock):
                block.update_command()
            script.append(block.command)
        script.append(partial(self.character.move, 0))
        self.script.set_script(script)

    def run(self, event_list):
        """
        The method executed on each iteration of the main game loop.
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """

        restart = False

        # Draw the drag and drop panels
        self.drag.draw()
        self.drop.draw()

        # Update the blocks
        from_drag = self.drag.update2(event_list)
        from_drop = self.drop.update2(event_list)
        self.to_drag(from_drop, DESTROY)
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
                    self.update_script()
                    self.script.start()
                    restart = True
        self.script.update()
        return restart
