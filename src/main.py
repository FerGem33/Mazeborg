import sys
import pygame
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.fullscreen = False
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(NAME)
        self.clock = pygame.time.Clock()
        self.level = Level()

    def toggle_fullscreen(self):
        # Toggle fullscreen state
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # Switch to fullscreen using the first available fullscreen mode
            pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            # Switch back to windowed mode with the original window size
            pygame.display.set_mode((WIDTH, HEIGHT))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()

            self.display.fill((113, 221, 238))
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
