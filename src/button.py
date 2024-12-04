import pygame


class Button:
    def __init__(self, display, img, pos):
        self.display = display
        self.surface = pygame.image.load(img).convert_alpha()
        self.rect = self.surface.get_rect(topleft=pos)

    def run(self, event_list):
        self.display.blit(self.surface, self.rect)
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
        return False
