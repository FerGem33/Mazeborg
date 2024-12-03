import sys
from settings import *
from support import load_level_list
from menu import Menu, SettingsMenu
from game import Game


class Main:
    def __init__(self):
        # Screen
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(NAME)
        icon = pygame.image.load('assets/images/robot/down_idle/idle_down.png')
        pygame.display.set_icon(icon)

        # Music
        volumes = {
            'bgm': 0.0,
            'sfx': 1.0
        }
        for key in list(CHANNELS.keys()):
            CHANNELS[key].set_volume(volumes[key])
        CHANNELS['bgm'].load(BGM['forest_lost'])

        # States
        self.state = 'main_menu'
        self.main_menu = Menu(["Iniciar", "Elegir nivel", "Ajustes", "Salir"])

        self.levels = load_level_list()
        self.selected_level = self.levels[0]
        self.level_menu = Menu(self.levels)

        settings = {
            'Volumen de Musica': CHANNELS['bgm'].get_volume(),
            'Volumen de Efectos de Sonido': CHANNELS['sfx'].get_volume(),
            'Volver a inicio': None
        }
        options = list(settings.keys())

        self.settings_menu = SettingsMenu(options, settings)

        self.game = None

    def handle_menu(self, option):
        if option[1]:
            if option[1] == 'Volver a inicio':
                self.state = 'main_menu'
        CHANNELS['bgm'].set_volume(option[0]['Volumen de Musica'])
        CHANNELS['sfx'].set_volume(option[0]['Volumen de Efectos de Sonido'])

    def run(self):
        CHANNELS['bgm'].play(-1)

        while True:
            event_list = pygame.event.get()

            match self.state:
                case 'main_menu':
                    option = self.main_menu.run(event_list)
                    match option:
                        case 'Iniciar':
                            self.game = Game(self.selected_level)
                            self.state = 'game'
                        case 'Elegir nivel':
                            self.state = 'level_menu'
                        case 'Ajustes':
                            self.state = 'settings_menu'
                        case 'Salir':
                            pygame.quit()
                            sys.exit()

                case 'level_menu':
                    option = self.level_menu.run(event_list)
                    if option:
                        self.selected_level = self.level_menu.run(event_list)
                        self.state = 'main_menu'

                case 'settings_menu':
                    option = self.settings_menu.run(event_list)
                    self.handle_menu(option)

                case 'game':
                    option = self.game.run(event_list)
                    self.handle_menu(option)

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
