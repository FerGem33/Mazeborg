import pygame


class CodeBlock(pygame.sprite.Sprite):
    """
    A block of code that is used to control the character's behaviour.
    """
    def __init__(self, pos, panel, draw_surface, fill_color, size=(170, 40)):
        """
        Parameters
        ----------
        pos : tuple
        Relative position of the block to its drawing surface.
        panel : Panel
        The panel that the block belongs to.
        draw_surface : pygame.Surface
        The surface to draw the block on.
        fill_color : pygame.color | str
        The fill color of the block.
        size : tuple
        The width and height of the block in pixels.
        """
        super().__init__()
        self.image = pygame.surface.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.panel = panel
        self.draw_surface = draw_surface
        self.fill_color = fill_color

        # update
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.moved = False

    def abs_rect(self) -> pygame.rect.Rect:
        """Returns the absolute rect with respect to the pygame display."""
        rect = self.rect.copy()
        rect.x += self.panel.offset[0]
        rect.y += self.panel.offset[1]
        return rect

    def update(self, event_list) -> bool:
        """
        Updates the block on mouse events, returns true if the block is moved out of its panel.
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """
        for event in event_list:
            # if mouse left button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # check if the block is clicked
                if self.abs_rect().collidepoint(event.pos):
                    self.dragging = True
                    self.moved = False
                    self.offset_x = self.rect.x - event.pos[0]
                    self.offset_y = self.rect.y - event.pos[1]

            # if mouse button is released
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dragging:
                    self.dragging = False
                    # return true if the block was released and moved out of its panel
                    return self.moved and not self.abs_rect().colliderect(self.panel.abs_rect())

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                # Update block position while dragging
                self.moved = True
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y

    def draw(self):
        """
        Draws the block on its draw surface.
        """
        self.image.fill(self.fill_color)
        self.draw_surface.blit(self.image, self.rect)
