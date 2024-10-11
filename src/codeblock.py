import pygame
from settings import *


class CodeBlock(pygame.sprite.Sprite):
    def __init__(self, pos, panel, width=170, height=40, fill_color='darkgreen'):
        super().__init__()
        self.image = pygame.surface.Surface((width, height))
        self.image.fill(fill_color)
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False
        self.panel = panel

        # update
        self.offset_x = 0
        self.offset_y = 0

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if the block is clicked
                    if self.panel == 'drag':
                        if self.rect.collidepoint(event.pos[0] - GAME_WIDTH - DROP_WIDTH, event.pos[1]):
                            self.dragging = True
                            self.offset_x = self.rect.x - event.pos[0]
                            self.offset_y = self.rect.y - event.pos[1]
                    elif self.panel == 'drop':
                        if self.rect.collidepoint(event.pos[0] - GAME_WIDTH, event.pos[1]):
                            self.dragging = True
                            self.offset_x = self.rect.x - event.pos[0]
                            self.offset_y = self.rect.y - event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                # Update block position while dragging
                # self.rect.move_ip(event.rel)
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y
