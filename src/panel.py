import pygame


class Panel:
    def __init__(self, pos, width, height, fill_color):
        self.display = pygame.display.get_surface()
        self.surface = pygame.surface.Surface((width, height))
        self.fill_color = fill_color
        self.rect = pygame.Rect(pos, (width, height))

        self.visible_sprites = pygame.sprite.Group()

    def run(self):
        pass
