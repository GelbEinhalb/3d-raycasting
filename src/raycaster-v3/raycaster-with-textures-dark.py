import math
import numpy as np
import pygame
from typing import Tuple

pygame.init()


class Raycaster:
    def __init__(self, map_path: str, texture_path: str, window_size: Tuple[int, int] = (700, 650)):
        # Load map, textures, and images
        self.map = np.load(map_path)
        self.textures = np.load(texture_path)

        # Window setup
        self.win_x, self.win_y = window_size
        self.screen = pygame.display.set_mode((self.win_x, self.win_y))
        pygame.display.set_caption("Raycaster by Pascal and Yannick")
        self.p_logo = pygame.image.load("images/logo.png")
        pygame.display.set_icon(self.p_logo)

        # Load images
        floor_image = pygame.image.load("images/floor.png").convert_alpha()
        self.floor = pygame.transform.scale(floor_image, (self.win_x, int(self.win_y / 2)))
        sky_image = pygame.image.load("images/sky.png").convert_alpha()
        self.sky = pygame.transform.scale(sky_image, (self.win_x, int(self.win_y / 2)))

        # Constants
        self.pi = math.pi
        self.max_fps = 30
        self.move_speed = 0.2
        self.rotation_speed = math.radians(3)
        self.line_width = 1
        self.num_rays = int(self.win_x / self.line_width) + 1
        self.field_of_view = math.radians(50)
        self.ray_density = self.field_of_view / (self.num_rays - 1)
        self.size = 800
        self.brightness = 4
        self.texture_shape = 30

        # Player position and direction
        self.player_x = 2.01
        self.player_y = 47.01
        self.direction = math.radians(45.01)

        # Setup the game clock
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.clock.tick(self.max_fps)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Handle key presses
            keys = pygame.key.get_pressed()

            # Move forward
            if keys[pygame.K_UP]:
                self.move_player(forward=True)

            # Move backward
            if keys[pygame.K_DOWN]:
                self.move_player(forward=False)

            # Rotate right
            if keys[pygame.K_RIGHT]:
                self.rotate_player(right=True)

            # Rotate left
            if keys[pygame.K_LEFT]:
                self.rotate_player(right=False)

            # Draw floor and sky
            self.screen.fill((127, 127, 255))
            self.screen.blit(self.sky, (0, 0))
            self.screen.blit(self.floor, (0, self.win_y / 2))

            # Cast rays
            self.cast_rays()

            # Update the display
            pygame.display.flip()

        pygame.display.quit()

    def move_player(self, forward: bool):
        sin_dir = math.sin(self.direction)
        cos_dir = math.cos(self.direction)
        if forward:
            if not self.map[int(self.player_y)][int(self.player_x + 0.6 * cos_dir)]:
                self.player_x += self.move_speed * cos_dir
            if not self.map[int(self.player_y - 0.6 * sin_dir)][int(self.player_x)]:
                self.player_y -= self.move_speed * sin_dir
        else:
            if not self.map[int(self.player_y)][int(self.player_x - self.move_speed * cos_dir)]:
                self.player_x -= self.move_speed * cos_dir
            if not self.map[int(self.player_y + self.move_speed * sin_dir)][int(self.player_x)]:
                self.player_y += self.move_speed * sin_dir

    def rotate_player(self, right: bool):
        if right:
            self.direction += self.rotation_speed
        else:
            self.direction -= self.rotation_speed
        self.direction %= 2 * self.pi

    def cast_rays(self):
        column = 0
        ray_direction = self.direction - self.field_of_view / 2

        for i in range(self.num_rays):
            ray_block_x = int(self.player_x)
            ray_block_y = int(self.player_y)

            # Ray direction in degrees
            ray_deg = math.degrees(ray_direction) % 360

            # North
            if 0 < ray_deg < 180:
                horizontal_x = self.player_x + (self.player_y % 1) / math.tan(ray_direction)
                delta_x = 1 / math.tan(ray_direction)
                vz_y = -1
            # South
            else:
                horizontal_x = self.player_x + (self.player_y % 1 - 1) / math.tan(ray_direction)
                delta_x = -1 / math.tan(ray_direction)
                vz_y = 1

            # East
            if ray_deg > 270 or ray_deg < 90:
                vertical_x = math.ceil(self.player_x)
                vz_x = 1
            # West
            else:
                vertical_x = math.floor(self.player_x)
                vz_x = -1

            wall_hit = False
            while not wall_hit:
                if horizontal_x * vz_x < vertical_x * vz_x:
                    intersection_x = horizontal_x
                    horizontal_x += delta_x
                    ray_block_y += vz_y
                    side = 0
                else:
                    intersection_x = vertical_x
                    vertical_x += vz_x
                    ray_block_x += vz_x
                    side = 1

                # Ray hits a wall?
                if self.map[ray_block_y][ray_block_x]:
                    wall_type = int(self.map[ray_block_y][ray_block_x])
                    wall_hit = True

            # Calculate the length of the ray
            ray_length = (intersection_x - self.player_x) / math.cos(ray_direction)

            # Distance to the wall (without fisheye effect)
            distance = ray_length * math.cos(ray_direction - self.direction)

            # Calculate the height of the column
            column_height = self.size / distance
            draw_start = (self.win_y / 2) - (column_height / 2)
            draw_end = (self.win_y / 2) + (column_height / 2)

            # Select the wall texture (including shading)
            texture = self.textures[wall_type - 1, side]

            # Select the correct texture column
            if side:
                intersection_y = abs(self.player_y - math.sin(ray_direction) * ray_length)
                texture_column = texture[:, int((intersection_y % 1) / (1 / self.texture_shape))]
            else:
                texture_column = texture[:, int((intersection_x % 1) / (1 / self.texture_shape))]

            # Calculate pixel height
            pixel_height = column_height / self.texture_shape

            for i, texture_pixel in enumerate(texture_column):
                start = i * pixel_height + draw_start
                end = start + pixel_height

                # Ensure the pixel line stays within screen bounds
                if start < self.win_y and end > 0:
                    if start < 0: start = 0
                    if end > self.win_y: end = self.win_y

                    # Adjust color based on distance (brightness)
                    color_factor = self.brightness / distance
                    if color_factor > 1:
                        color_factor = 1
                    color = texture_pixel * color_factor

                    # Draw the pixel line
                    pygame.draw.line(self.screen, color, (column, start), (column, end), self.line_width)

            # Update for next ray
            ray_direction += self.ray_density
            column += self.line_width


# Initialize and run the game
if __name__ == "__main__":
    raycaster = Raycaster(map_path="maps/map1.npy", texture_path="textures/textures30.npy")
    raycaster.run()
