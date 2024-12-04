import pygame.mixer_music
from settings import *
from level import Level
from menu import SettingsMenu
from button import Button


class Game:
    def __init__(self, level_name):
        self.clock = pygame.time.Clock()
        self.paused = False

        settings = {
            'Volver al juego': None,
            'Volumen de Musica': CHANNELS['bgm'].get_volume(),
            'Volumen de Efectos de Sonido': CHANNELS['sfx'].get_volume(),
            'Camara sigue al jugador': CAMERA_FOLLOW,
            'Volver a inicio': None
        }
        options = list(settings.keys())
        self.pause_menu = SettingsMenu(options, settings)

        # Panels
        self.level = Level(level_name)
        self.level.always_follow = settings['Camara sigue al jugador']

        # Buttons
        display = pygame.display.get_surface()
        self.menu_bttn = Button(display, 'assets/images/icons/menu.png', (30, 30))
        self.play_bttn = Button(display, 'assets/images/icons/play.png', (90, 30))

    def run(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.paused = True

        option = self.pause_menu.run(event_list, self.paused)
        if self.paused:
            if option[1]:
                if option[1] == 'Volver al juego':
                    self.paused = False
            self.level.always_follow = option[0]['Camara sigue al jugador']
        else:
            self.level.run(event_list)
            if self.menu_bttn.run(event_list):
                self.paused = True
            if self.play_bttn.run(event_list):
                self.level.dragdrop.update_script()
                self.level.dragdrop.script.start()
                self.level.restart()

        if option[1] == 'Volver a inicio':
            option[0] = None

        self.clock.tick(FPS)
        return option
