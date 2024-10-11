from support import *
from game import Game
from drag_and_drop import DragAndDrop


class Level:
    def __init__(self):
        # Screen and panels
        self.display = pygame.display.get_surface()

        self.game = Game()
        self.dragdrop = DragAndDrop()

    def run(self, event_list):
        self.game.run()
        self.dragdrop.run(event_list)
