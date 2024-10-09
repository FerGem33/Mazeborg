import pygame
from support import *


class Robot(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collidable_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/images/robot/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.inflate(0, -26)

        # texturas
        self.animations = None
        self.import_textures()
        self.state = 'down'
        self.photogram_index = 0
        self.animation_speed = 0.15

        # movement and attack
        self.direction = pygame.math.Vector2()
        self.collidable_sprites = collidable_sprites
        self.attacking = False
        self.attack_reload_time = 400
        self.attack_time = None

    def import_textures(self):
        path = 'assets/images/robot/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}

        for animation in self.animations:
            fullpath = path + animation
            self.animations[animation] = import_folder(fullpath)

    def keys_input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            # movement
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.state = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.state = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.state = 'right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.state = 'left'
            else:
                self.direction.x = 0

            # stats
            self.stats = {'health': 10, 'energy': 60, 'attack': 10, 'magic': 4, 'velocity': 5}
            self.health = self.stats['health']
            self.energy = self.stats['energy']
            self.velocity = self.stats['velocity']
            self.exp = 123

    def get_state(self):
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.state and 'attack' not in self.state:
                self.state = self.state + '_idle'

        # attack
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'attack' not in self.state:
                if 'idle' in self.state:
                    self.state = self.state.replace('_idle', '_attack')
                else:
                    self.state = self.state + '_attack'
        else:
            if 'attack' in self.state:
                self.state = self.state.replace('_attack', '')

    def move(self, velocity):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * velocity
        self.collide('horizontal')
        self.hitbox.y += self.direction.y * velocity
        self.collide('vertical')
        self.rect.center = self.hitbox.center

    def collide(self, direction):
        if direction == 'horizontal':
            for sprite in self.collidable_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # eastward
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # westward
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.collidable_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # southward
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # northward
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        animation = self.animations[self.state]

        # loop
        self.photogram_index += self.animation_speed
        if self.photogram_index >= len(animation):
            self.photogram_index = 0

        # change image
        self.image = animation[int(self.photogram_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)


    def update(self):
        self.keys_input()
        # self.reload()
        self.get_state()
        self.animate()
        self.move(self.velocity)