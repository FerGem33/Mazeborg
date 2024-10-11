import pygame
from settings import *
from codeblock import CodeBlock


class DragAndDrop:
    def __init__(self):
        self.display = pygame.display.get_surface()

        self.drag_surf = pygame.Surface((DRAG_WIDTH, HEIGHT))
        self.drop_surf = pygame.Surface((DROP_WIDTH, HEIGHT))
        self.drag_rect = self.drag_surf.get_rect(topleft=(GAME_WIDTH + DROP_WIDTH, 0))
        self.drop_rect = self.drop_surf.get_rect(topleft=(GAME_WIDTH, 0))
        self.drag_color = 'cadetblue4'
        self.drop_color = 'cadetblue3'

        # CodeBlocks
        self.drag_blocks = pygame.sprite.Group()
        self.drop_blocks = pygame.sprite.Group()

        self.drop_blocks.add(CodeBlock((40, 30), 'drop'))
        self.drag_blocks.add(CodeBlock((40, 230), 'drag'))
        # self.add_block(CodeBlock((20, 30)), self.drag_blocks)

    def add_block(self, block, group):
        if group is self.drop_blocks:
            block.rect.x += GAME_WIDTH
        if group is self.drag_blocks:
            block.rect.x += GAME_WIDTH + DROP_WIDTH
        group.add(block)

    def run(self, event_list):
        # Fill the panels with its background color
        self.drag_surf.fill(self.drag_color)
        self.drop_surf.fill(self.drop_color)

        # Update the blocks
        self.drop_blocks.update(event_list)
        self.drag_blocks.update(event_list)

        # Draw the blocks into their panels
        self.drag_blocks.draw(self.drag_surf)
        self.drop_blocks.draw(self.drop_surf)

        # Draw the panels into the screen
        self.display.blit(self.drag_surf, self.drag_rect)
        self.display.blit(self.drop_surf, self.drop_rect)
