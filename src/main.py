import sys
import pygame
from settings import *
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        self.fullscreen = False
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(NAME)
        icon = pygame.image.load('assets/images/robot/down_idle/idle_down.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.level = Game()

        # Music
        self.volume = 0
        pygame.mixer.music.load(BGM1)
        pygame.mixer.music.set_volume(self.volume)

    def toggle_fullscreen(self):
        # Toggle fullscreen state
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # Switch to fullscreen using the first available fullscreen mode
            pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            # Switch back to windowed mode with the original window size
            pygame.display.set_mode((WIDTH, HEIGHT))

    def toggle_volume(self):
        if self.volume == 0:
            self.volume = 0.75
        else:
            self.volume = 0
        pygame.mixer.music.set_volume(self.volume)

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
                    if event.key == pygame.K_m:
                        self.toggle_volume()
            self.level.run(event_list)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    main = Main()
    main.run()
