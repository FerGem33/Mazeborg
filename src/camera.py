import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface):
        super().__init__()
        self.display = surface  # pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.ground_surf = pygame.image.load('assets/images/ground.png').convert()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def draw(self, robot):
        self.offset.x = robot.rect.centerx - self.half_width
        self.offset.y = robot.rect.centery - self.half_height

        ground_pos = self.ground_rect.topleft - self.offset
        self.display.blit(self.ground_surf, ground_pos)

        for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
            new_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, new_pos)