import pygame


pygame.init()
pygame.mixer.init()

# Game name
NAME = 'Mazeborg'

# Screen size
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

# Panels
GAME_WIDTH = int(WIDTH * 0.6)
DRAG_WIDTH = int(WIDTH * 0.2)
DROP_WIDTH = int(WIDTH * 0.2)

# Game settings
TILESIZE = 64
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Music
BGM = {
    'forest_lost': 'assets/sounds/Forever Lost.ogg',
    'groovy_booty': 'assets/sounds/Groovy booty.ogg'
}

# Sfx
CHANNELS = {
    'bgm': pygame.mixer.music,
    'sfx': pygame.mixer.Channel(0),
}

VOLUMES = {
    'bgm': 0.0,
    'sfx': 1.0,
}
SFX = {
    'menu1': pygame.mixer.Sound('assets/sounds/menu1.wav'),
    'accept': pygame.mixer.Sound('assets/sounds/select.ogg'),
    'cant': pygame.mixer.Sound('assets/sounds/cant.ogg'),
    'grab': pygame.mixer.Sound('assets/sounds/grab.wav'),
    'save': pygame.mixer.Sound('assets/sounds/save.ogg'),
    'adjust': pygame.mixer.Sound('assets/sounds/adjust.ogg'),
}

# Default values
DESTROY = True
CAMERA_FOLLOW = False
