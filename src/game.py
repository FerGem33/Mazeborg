import pygame.mixer_music
from settings import *
from level import Level
from menu import SettingsMenu


class Game:
    def __init__(self, level_name):
        self.clock = pygame.time.Clock()
        self.paused = False

        settings = {
            'Volver al juego': None,
            'Volumen de Musica': CHANNELS['bgm'].get_volume(),
            'Volumen de Efectos de Sonido': CHANNELS['sfx'].get_volume(),
            'Camara sigue al jugador': True,
            'Volver a inicio': None
        }
        options = list(settings.keys())
        self.pause_menu = SettingsMenu(options, settings)

        # Panels
        self.level = Level(level_name)

    def run(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.paused = True

        option = self.pause_menu.run(event_list)
        if option[1]:
            if option[1] == 'Volver al juego':
                self.paused = False
        self.level.always_follow = option[0]['Camara sigue al jugador']

        if not self.paused:
            self.level.run(event_list)

        self.clock.tick(FPS)
        return option
