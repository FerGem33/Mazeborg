import pygame


class CameraGroup(pygame.sprite.Group):
    """
    A special Group that draws its sprites around the character and sorted by the y axis.
    """
    def __init__(self, draw_surface):
        """
        Parameters
        ----------
        draw_surface : pygame.Surface
        The surface to draw the sprites on
        """
        super().__init__()
        self.draw_surface = draw_surface  # pygame.display.get_surface()
        self.half_width = self.draw_surface.get_size()[0] // 2
        self.half_height = self.draw_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def draw(self, robot):
        self.offset.x = robot.rect.centerx - self.half_width
        self.offset.y = robot.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
            new_pos = sprite.rect.topleft - self.offset
            self.draw_surface.blit(sprite.image, new_pos)