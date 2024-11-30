from support import *
from settings import *


class Character(pygame.sprite.Sprite):
    """
    The character controlled by the player.
    """

    def __init__(self, pos, groups, collidable_sprites):
        """
        Parameters
        ----------
        pos : tuple
        Relative position of the player to its draw surface.
        groups : pygame.sprite.Group
        The sprite groups the character belongs to.
        collidable_sprites : pygame.sprite.Group
        The group containing the sprites that the character can collide with.
        """
        super().__init__(groups)
        self.spawn = pos
        self.image = pygame.image.load('assets/images/robot/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=self.spawn)
        self.hitbox = self.rect.inflate(0, -26)

        # movement
        self.direction = pygame.math.Vector2(0, 1)
        self.velocity = 6
        self.collidable_sprites = collidable_sprites

        # Animations
        self.animations = None
        self.import_textures()
        self.state = 'down_idle'
        self.photogram_index = 0
        self.animation_speed = 0.15

        # script
        self.executing_command = False
        self.progress = 0
        self.duration = 0

    def import_textures(self):
        """
        Import the sprites of the character and stores them in the dictionary self.animations.
        """
        path = 'assets/images/robot/'

        # Each key represents a state, and its value is a list of all sprites of that states.
        # Each list is intended to be iterated to produce the effect of motion in the animation.
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}

        for animation in self.animations:
            fullpath = path + animation
            self.animations[animation] = import_folder(fullpath)

    def restart(self):
        self.rect = self.image.get_rect(topleft=self.spawn)
        self.hitbox = self.rect.inflate(0, -26)

        self.direction = pygame.math.Vector2(0, 1)
        self.state = 'down_idle'

        self.executing_command = False
        self.progress = 0
        self.duration = 0

        self.update()

    def update_state(self):
        """
        Update the state of the character according to its direction and action being performed.
        """

        # if the character is not performing any action
        if self.progress == 0:
            if 'idle' not in self.state:
                self.state += '_idle'
        else:
            # if the direction is positive in y
            if self.direction.y > 0:
                self.state = 'down'
            # if the direction is negative in y
            elif self.direction.y < 0:
                self.state = 'up'
            # if the direction is positive in x
            if self.direction.x > 0:
                self.state = 'right'
            # if the direction is negative in x
            elif self.direction.x < 0:
                self.state = 'left'

    def animate(self):
        """
        Animates the character.
        """
        # Select the current animation based on state
        self.update_state()
        animation = self.animations[self.state]

        # Iterate over the sprites in current animation
        self.photogram_index += self.animation_speed
        if self.photogram_index >= len(animation):
            self.photogram_index = 0

        # Change the current image of the character
        self.image = animation[int(self.photogram_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()

    # Methods to control the character via scripts
    def collide(self, direction):
        """
        Check for collision between the character and its collidable sprites.
        direction: str
        The axis to check collisions in.
        """
        for sprite in self.collidable_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'x':
                    if self.direction.x > 0:  # eastward
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # westward
                        self.hitbox.left = sprite.hitbox.right
                elif direction == 'y':
                    if self.direction.y > 0:  # southward
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # northward
                        self.hitbox.top = sprite.hitbox.bottom
                return True

    def sensor(self, direction, distance: int = TILESIZE):
        """
        Check if the chracter is one tile away from an obstacle.
        direction: str
        The axis to check collisions in.
        distance: int
        The distance in px to check for obstacles.
        """
        hitbox = self.hitbox
        hitbox.x += self.direction[0] * distance
        hitbox.y += self.direction[1] * distance

        for sprite in self.collidable_sprites:
            if sprite.hitbox.colliderect(hitbox):
                if direction == 'x':
                    if self.direction.x > 0:  # eastward
                        self.hitbox.right = sprite.hitbox.left - distance
                    if self.direction.x < 0:  # westward
                        self.hitbox.left = sprite.hitbox.right - distance
                elif direction == 'y':
                    if self.direction.y > 0:  # southward
                        self.hitbox.bottom = sprite.hitbox.top - distance
                    if self.direction.y < 0:  # northward
                        self.hitbox.top = sprite.hitbox.bottom - distance
                return True

    def forward(self):
        """
        Move the character one step in its current direction.
        """
        # Normalize the direction vector so that the velocity is always the same
        if self.direction.magnitude() != 0:
            self.direction.normalize_ip()

        # Move the character's hitbox and check for collisions

        self.hitbox.x += self.direction.x * self.velocity
        collided = self.collide('x')
        self.hitbox.y += self.direction.y * self.velocity
        collided = collided or self.collide('y')
        return collided

    def move(self, tiles):
        """
        Move the character in its current direction until the given number of tiles are traveled.
        Parameters
        ----------
        tiles : int
        The number of tiles to move.
        """
        self.duration = int(tiles * TILESIZE / self.velocity)
        if self.progress <= self.duration:
            self.forward()
            self.progress += 1
            return False
        else:
            self.progress = 0
            return True

    def rotate(self, angle):
        """
        Rotates the direction vector of the player by the given angle.
        Parameters
        ----------
        angle : float
        The angle in degrees to rotate by.
        """
        self.direction.rotate_ip(angle)
        return True

    def smart_move(self):
        self.progress = 1
        if self.forward():
            self.progress = 0
            return True
        return False
