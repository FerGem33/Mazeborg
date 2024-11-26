from level import Level
from drag_and_drop import DragAndDrop


class Game:
    def __init__(self):
        # Panels
        self.level = Level()

    def run(self, event_list):
        """
        The method executed on each iteration of the main game loop.
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """
        self.level.run(event_list)

