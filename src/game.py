from level import Level
import pygame


class Game:
    def __init__(self):
        # Panels
        self.sounds = {
            'cant': pygame.mixer.Sound('assets/sounds/cant.ogg'),
            'grab': pygame.mixer.Sound('assets/sounds/grab.wav'),
        }
        self.level = Level(self.sounds)

    def run(self, event_list):
        """
        The method executed on each iteration of the main game loop.
        Parameters
        ----------
        event_list : list
        The list of events received from the pygame display.
        """
        self.level.run(event_list)

