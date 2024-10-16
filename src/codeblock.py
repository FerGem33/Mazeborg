import pygame
from functools import partial
from time import time
from support import load_icon
from character import Character


class CodeBlock:
    """
    A block of code that controls the character's behavior.
    """

    def __init__(self, pos, panel, draw_surface, block_type, character):
        """
        Parameters
        ----------
        pos : tuple
            Relative position of the block to its drawing surface.
        panel : Panel
            The panel that the block belongs to.
        draw_surface : pygame.Surface
            The surface to draw the block on.
        block_type : str
            The type of the block (e.g., 'start', 'finish', etc.).
        character : Character
        The character that the block controls.
        """
        self.rect = pygame.Rect(pos, (170, 60))
        self.panel = panel
        self.draw_surface = draw_surface
        self.block_type = block_type
        self.character = character

        # Block types and their properties
        types = {
            # key: [fill_color, icon, function]
            'start': ['#389C9A', 'start.png', None],
            'finish': ['#F23C4D', 'finish.png', None],
            'movex': ['#52489C', 'movex.png', self.character.move],
            'rotatex': ['#4062BB', 'rotatex.png', self.character.rotate],
        }

        self.fill_color = types[block_type][0]
        self.icon = load_icon(types[block_type][1], (40, 40))
        self.function = types[block_type][2]

        # Dragging-related attributes
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.moved = False

        # Command to be executed by the block
        self.args = []
        self.command = None

    def draw(self):
        """Draws the block on its draw surface, including the icon and input box if applicable."""
        pygame.draw.rect(self.draw_surface, self.fill_color, self.rect, border_radius=10)
        self.draw_icon()

    def update(self, event_list) -> bool:
        """
        Updates the block on mouse events and checks if it's moved out of its panel.
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.abs_rect().collidepoint(event.pos):
                    self.dragging = True
                    self.moved = False
                    self.offset_x = self.rect.x - event.pos[0]
                    self.offset_y = self.rect.y - event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dragging:
                    self.dragging = False
                    return self.moved and not self.abs_rect().colliderect(self.panel.abs_rect())

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                # Update block position while dragging
                self.moved = True
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y

    def run(self, event_list):
        """
        The method executed on each iteration of the main game loop.
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """
        return self.update(event_list)

    def abs_rect(self) -> pygame.Rect:
        """Returns the absolute position of the block with respect to the pygame display."""
        rect = self.rect.copy()
        rect.x += self.panel.offset[0]
        rect.y += self.panel.offset[1]
        return rect

    def update_args(self, args):
        """
        Sets the arguments for the block's command and updates it.
        Parameters
        ----------
        args : str
        The string that contains the arg to be updated.
        """
        try:
            args = int(args)
        except ValueError:
            try:
                args = float(args)
            except ValueError:
                pass
        self.args = args

    def draw_icon(self):
        """Draws the icon at the appropriate position."""
        icon_rect = self.icon.get_rect(center=self.rect.center)
        self.draw_surface.blit(self.icon, icon_rect)


class InputBlock(CodeBlock):
    """
    A block of code that allows user text-input.
    """

    def __init__(self, pos, panel, draw_surface, block_type, character):
        """
        Parameters
        ----------
        pos : tuple
            Relative position of the block to its drawing surface.
        panel : Panel
            The panel that the block belongs to.
        draw_surface : pygame.Surface
            The surface to draw the block on.
        block_type : str
            The type of the block (e.g., 'start', 'finish', etc.).
        """
        super().__init__(pos, panel, draw_surface, block_type, character)

        # Input text and box for blocks that have input (e.g., 'movex', 'rotatex')
        self.text = ''
        self.input_active = False
        self.input_rect = pygame.Rect(self.rect.right - 100, self.rect.top + 10, 80, 40)
        self.cursor_visible = True
        self.cursor_time = time()
        self.font = pygame.font.Font('assets/fonts/monogram.ttf', 45)

        self.update_command()

    def draw(self):
        """Draws the block on its draw surface, including the icon and input box"""
        pygame.draw.rect(self.draw_surface, self.fill_color, self.rect, border_radius=10)
        self.draw_icon()
        self.draw_input_box()

    def run(self, event_list) -> bool:
        """
        Runs the block.
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """
        self.handle_input(event_list)
        if time() - self.cursor_time > 0.5:  # Change every half second
            self.cursor_visible = not self.cursor_visible
            self.cursor_time = time()
        return self.update(event_list)

    def draw_icon(self):
        """Draws the icon at the appropriate position."""
        icon_rect = self.icon.get_rect(topleft=(self.rect.x + 10, self.rect.y + 10))
        self.draw_surface.blit(self.icon, icon_rect)

    def draw_input_box(self):
        """Draws the input box."""

        # Draw input box
        rect = pygame.Rect(self.rect.right - 100, self.rect.top + 10, 80, 40)
        pygame.draw.rect(self.draw_surface, (200, 200, 200), rect)

        # Render and draw text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.draw_surface.blit(text_surface, (rect.x + 10, rect.y))

        # If the input is active, draw the blinking cursor at the end of the text
        if self.input_active and self.cursor_visible:
            cursor_x = rect.x + text_surface.get_width() + 10  # Position after the text
            pygame.draw.line(self.draw_surface, (0, 0, 0), (cursor_x, rect.y + 5), (cursor_x, rect.y + 35), 2)

    def abs_input_rect(self) -> pygame.Rect:
        """Returns the absolute position of the input rect."""
        if self.input_rect:
            rect = self.input_rect.copy()
            rect.x += self.panel.offset[0]
            rect.y += self.panel.offset[1]
            return rect

    def update_command(self):
        """Sets the command for the block based on its type."""
        if self.text:
            self.update_args(self.text)
        if self.function:
            self.command = partial(self.function, self.args)

    def update_args(self, args):
        """Sets the arguments for the block's command and updates it."""
        try:
            args = int(args)
        except ValueError:
            try:
                args = float(args)
            except ValueError:
                pass
        self.args = args

    def handle_input(self, event_list):
        """
        Handles user input for the input box.
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect and self.abs_input_rect().collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False

            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Remove last character
                else:
                    self.text += event.unicode  # Add new character
