from settings import *
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

        self.dragging = False
        self.last_mouse_pos = None
        self.offset = pygame.math.Vector2()
        self.camera_offset = pygame.math.Vector2()
        self.camera_velocity = 0.5

        self.follow_character = True

        self.last_camera_toggle = 0
        self.toggle_delay = 300

        # Zoom variables
        self.zoom = 1.00
        self.target_zoom = 1.00
        self.zoom_speed = 0.1
        self.min_zoom = 0.5
        self.max_zoom = 1.0

    def toggle_camera(self):
        self.follow_character = True

    def handle_input(self, event_list):
        """
        Handle input for camera movement and mode switching.
        """
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Current time in milliseconds

        # Focus character
        if keys[pygame.K_c] and current_time - self.last_camera_toggle > self.toggle_delay:
            self.last_camera_toggle = current_time
            self.toggle_camera()

        for event in event_list:
            if pygame.mouse.get_pos()[0] < GAME_WIDTH:
                # Drag camera
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.dragging = True
                    self.last_mouse_pos = event.pos

                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    self.camera_offset[0] += (event.pos[0] - self.last_mouse_pos[0]) / self.zoom
                    self.camera_offset[1] += (event.pos[1] - self.last_mouse_pos[1]) / self.zoom
                    self.camera_offset *= self.camera_velocity
                    self.last_mouse_pos = event.pos

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.dragging:
                        self.camera_offset = pygame.math.Vector2()
                        self.dragging = False

                # Zoom camera
                elif event.type == pygame.MOUSEWHEEL:
                    self.target_zoom += event.y * 0.05
                    self.target_zoom = max(self.min_zoom, min(self.max_zoom, self.target_zoom))

    def apply_smooth_zoom(self):
        """
        Gradually approach the target zoom level for smooth scaling.
        Adjust offset to maintain focus during zooming.
        """
        if self.zoom != self.target_zoom:
            zoom_change = (self.target_zoom - self.zoom) * self.zoom_speed
            self.zoom += zoom_change

            # Adjust the offset to keep the camera centered
            mouse_x, mouse_y = pygame.mouse.get_pos()
            offset_change_x = (mouse_x - self.half_width) * zoom_change / self.zoom
            offset_change_y = (mouse_y - self.half_height) * zoom_change / self.zoom
            self.offset.x -= offset_change_x
            self.offset.y -= offset_change_y

    def return_to_center(self, robot, smooth=True):
        if smooth:
            target_x = robot.rect.centerx - self.half_width
            target_y = robot.rect.centery - self.half_height
            self.offset.x += (target_x - self.offset.x) * 0.05
            self.offset.y += (target_y - self.offset.y) * 0.05
        else:
            self.offset.x = robot.rect.centerx - self.half_width
            self.offset.y = robot.rect.centery - self.half_height

    def update_camera(self, robot):
        """
        Update camera position based on centering or manual movement.
        """
        self.apply_smooth_zoom()

        if self.follow_character:
            self.return_to_center(robot, smooth=True)
            # Stop centering once close enough to the target
            if abs(self.offset.x - (robot.rect.centerx - self.half_width)) < 1 and \
               abs(self.offset.y - (robot.rect.centery - self.half_height)) < 1:
                self.follow_character = False
        else:
            self.offset -= self.camera_offset

    def draw(self, robot, event_list):
        """
        Draw sprites with the current offset and smooth zoom handling.
        """
        self.handle_input(event_list)
        self.update_camera(robot)

        # Draw all sprites sorted by Y axis
        for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
            # Calculate scaled position and size
            scaled_rect = sprite.rect.inflate(
                sprite.rect.width * (self.zoom - 1),
                sprite.rect.height * (self.zoom - 1)
            )
            scaled_rect.topleft = (
                (sprite.rect.x - self.offset.x) * self.zoom,
                (sprite.rect.y - self.offset.y) * self.zoom,
            )

            # Convert positions to integers to avoid subpixel artifacts
            scaled_rect.topleft = (int(scaled_rect.topleft[0]), int(scaled_rect.topleft[1]))

            # Scale the sprite image
            scaled_image = pygame.transform.smoothscale(sprite.image, (int(scaled_rect.width), int(scaled_rect.height)))

            # Draw the sprite on the surface
            self.draw_surface.blit(scaled_image, scaled_rect.topleft)

