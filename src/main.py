import sys
import pygame
from settings import *
from level import Level


class Main:
    def __init__(self):
        pygame.init()
        self.fullscreen = False
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(NAME)
        icon = pygame.image.load('assets/images/robot/down_idle/idle_down.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.level = Level()

        pygame.mixer.music.load(BGM1)

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
        pygame.mixer.music.play(loops=int(1e6))

        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()

            self.level.run(event_list)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    main = Main()
    main.run()
