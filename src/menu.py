import pygame
from settings import SFX, CHANNELS


class Menu:
    def __init__(self, options, fill_color=(0, 0, 0)):
        self.display = pygame.display.get_surface()
        self.options = options
        self.fill_color = fill_color
        self.selected_index = 0

        self.font = pygame.font.Font('assets/fonts/monogram.ttf', 50)

    def draw(self):
        self.display.fill(self.fill_color)  # Black background
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_index else (100, 100, 100)
            text = self.font.render(option, True, color)
            self.display.blit(text, (200, 100 + 60 * i))

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                    CHANNELS['sfx'].play(SFX['menu1'])
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                    CHANNELS['sfx'].play(SFX['menu1'])
                elif event.key == pygame.K_RETURN:
                    CHANNELS['sfx'].play(SFX['accept'])
                    return self.options[self.selected_index]
        return None

    def run(self, event_list):
        self.draw()
        return self.update(event_list)


class SettingsMenu(Menu):
    def __init__(self, options, settings, fill_color=(0, 0, 0)):
        """
        Parameters
        ----------
        options : list
            A list of option names.
        settings : dict
            A dictionary of settings with keys as option names and values as their states.
            States can be:
                - float (e.g., for sliders, representing volume levels between 0.0 and 1.0)
                - bool (e.g., for toggle options, True/False)
        fill_color : tuple
            The background color of the menu.
        """
        super().__init__(options, fill_color)
        self.settings = settings  # Store settings
        self.option = None

    def draw(self):
        self.display.fill(self.fill_color)
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_index else (100, 100, 100)
            text = self.font.render(option, True, color)
            self.display.blit(text, (200, 100 + 60 * i))

            # Draw current state for sliders or toggles
            if isinstance(self.settings[option], float):  # Slider
                slider_x = 850
                slider_y = 115 + 60 * i
                slider_width = 200
                pygame.draw.rect(self.display, (150, 150, 150), (slider_x, slider_y, slider_width, 10))
                fill_width = int(self.settings[option] * slider_width)
                pygame.draw.rect(self.display, (255, 255, 255), (slider_x, slider_y, fill_width, 10))
            elif isinstance(self.settings[option], bool):  # Toggle
                toggle_text = "Si" if self.settings[option] else "No"
                toggle_color = (0, 255, 0) if self.settings[option] else (255, 0, 0)
                toggle_display = self.font.render(toggle_text, True, toggle_color)
                self.display.blit(toggle_display, (700, 100 + 60 * i))

    def update(self, event_list, menu_active):
        if menu_active:
            for event in event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                        CHANNELS['sfx'].play(SFX['menu1'])
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                        CHANNELS['sfx'].play(SFX['menu1'])
                    elif event.key == pygame.K_RIGHT:
                        self.adjust_setting(1)
                    elif event.key == pygame.K_LEFT:
                        self.adjust_setting(-1)
                    elif event.key == pygame.K_RETURN:
                        if self.settings[self.options[self.selected_index]] is not None:
                            self.adjust_setting(0)
                        else:
                            SFX['accept'].play()
                            """if self.options[-1] == self.options[self.selected_index]:
                                return self.settings
                            return self.options[self.selected_index]"""
                            return [self.settings, self.options[self.selected_index]]
        return [self.settings, None]

    def run(self, event_list, menu_active=True):
        self.draw()
        return self.update(event_list, menu_active)

    def adjust_setting(self, direction):
        """
        Adjust the selected setting.

        Parameters
        ----------
        direction : int
        1 to increase or toggle on; -1 to decrease or toggle off.
        """
        option = self.options[self.selected_index]
        if isinstance(self.settings[option], float):  # Slider
            self.settings[option] = max(0.0, min(1.0, self.settings[option] + 0.1 * direction))
            CHANNELS['sfx'].play(SFX['adjust'])
        elif isinstance(self.settings[option], bool):  # Toggle
            self.settings[option] = not self.settings[option]
            CHANNELS['sfx'].play(SFX['adjust'])
