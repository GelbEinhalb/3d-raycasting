import math
import pygame
from typing import List, Tuple

pygame.init()


class Raycaster:

    def __init__(self):
        # Constants
        self.WIN_X: int = 600
        self.WIN_Y: int = 600
        self.PI: float = math.pi
        self.MAX_FPS: int = 60
        self.MOVE_SPEED: float = 0.06
        self.ROTATE_SPEED: float = math.radians(1.3)
        self.LINE_WIDTH: int = 50
        self.NUM_RAYS: int = int(self.WIN_X / self.LINE_WIDTH) + 1
        self.FOV: float = math.radians(50)
        self.RAY_DENSITY: float = self.FOV / (self.NUM_RAYS - 1)
        self.SIZE: int = 400
        self.LIGHTNESS: int = 300
        self.SHADOW: int = 2

        # Player variables
        self.player_x: float = 7.2325
        self.player_y: float = 6.5866
        self.direction: float = 2.575

        # World map, where the player moves
        self.world_map: List[List[int]] = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.screen = pygame.display.set_mode((self.WIN_X * 2, self.WIN_Y))
        pygame.display.set_caption("Raycaster")
        self.clock = pygame.time.Clock()

    def move_player(self):
        keys = pygame.key.get_pressed()

        sin_direction = math.sin(self.direction)
        cos_direction = math.cos(self.direction)

        # Move up
        if keys[pygame.K_UP]:
            if not self.world_map[int(self.player_y)][int(self.player_x + self.MOVE_SPEED * cos_direction)]:
                self.player_x += self.MOVE_SPEED * cos_direction
            if not self.world_map[int(self.player_y - self.MOVE_SPEED * sin_direction)][int(self.player_x)]:
                self.player_y -= self.MOVE_SPEED * sin_direction

        # Move down
        if keys[pygame.K_DOWN]:
            if not self.world_map[int(self.player_y)][int(self.player_x - self.MOVE_SPEED * cos_direction)]:
                self.player_x -= self.MOVE_SPEED * cos_direction
            if not self.world_map[int(self.player_y + self.MOVE_SPEED * sin_direction)][int(self.player_x)]:
                self.player_y += self.MOVE_SPEED * sin_direction

        # Rotate left
        if keys[pygame.K_LEFT]:
            self.direction += self.ROTATE_SPEED
            self.direction %= 2 * self.PI

        # Rotate right
        if keys[pygame.K_RIGHT]:
            self.direction -= self.ROTATE_SPEED
            self.direction %= 2 * self.PI

    def cast_rays(self):
        ray_direction = self.direction - self.FOV / 2
        column = self.WIN_X * 2

        for _ in range(self.NUM_RAYS):
            ray_block_x = int(self.player_x)
            ray_block_y = int(self.player_y)
            ray_degree = math.degrees(ray_direction) % 360

            # Ray calculations
            if 0 < ray_degree < 180:
                horizontal_x = self.player_x + (self.player_y % 1) / math.tan(ray_direction)
                delta_x = 1 / math.tan(ray_direction)
                vz_y = -1
            else:
                horizontal_x = self.player_x + (self.player_y % 1 - 1) / math.tan(ray_direction)
                delta_x = -1 / math.tan(ray_direction)
                vz_y = 1

            if ray_degree > 270 or ray_degree < 90:
                vertical_x = math.ceil(self.player_x)
                vz_x = 1
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

                if self.world_map[ray_block_y][ray_block_x]:
                    texture = self.world_map[ray_block_y][ray_block_x]
                    wall_hit = True

            ray_length = (intersection_x - self.player_x) / math.cos(ray_direction)
            distance = ray_length * math.cos(ray_direction - self.direction)
            line_height = self.SIZE / distance
            draw_start = (self.WIN_Y / 2) - (line_height / 2)
            if draw_start < 0: draw_start = 0
            draw_end = (self.WIN_Y / 2) + (line_height / 2)
            if draw_end > self.WIN_Y: draw_end = self.WIN_Y

            brightness = int(-10 * distance + 200)
            brightness = max(0, brightness)  # Ensure brightness is not smaller than 0.
            if side: brightness //= 2
            color = (0, brightness, 0)

            # Draw line for ray visualization
            pygame.draw.line(self.screen, color, (column, draw_start), (column, draw_end), self.LINE_WIDTH)

            # Ray visualization on the left side
            ray_end_y = self.player_y - math.tan(ray_direction) * (intersection_x - self.player_x)
            pygame.draw.line(self.screen, (255, 255, 0),
                             (self.player_x * 60, self.player_y * 60),
                             (intersection_x * 60, ray_end_y * 60), 3)

            ray_direction += self.RAY_DENSITY
            column -= self.LINE_WIDTH

    def draw_map(self):
        for y in range(10):
            for x in range(10):
                if self.world_map[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x * 60, y * 60, 60, 60))
                    pygame.draw.rect(self.screen, (100, 100, 100), (x * 60, y * 60, 60, 60), 3)

    def draw_player(self):
        pygame.draw.circle(self.screen, (0, 255, 0), (int(self.player_x * 60), int(self.player_y * 60)), 8)

    def run(self):
        running = True
        while running:
            print(self.player_x, self.player_y, self.direction)
            self.clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Handle player movement
            self.move_player()

            # Draw the floor and ceiling
            self.screen.fill((180, 180, 180))
            pygame.draw.rect(self.screen, (170, 170, 170), (self.WIN_X, 0, self.WIN_X, self.WIN_Y))
            pygame.draw.rect(self.screen, (0, 0, 50), (self.WIN_X, 0, self.WIN_X, self.WIN_Y / 2))
            pygame.draw.rect(self.screen, (65, 40, 20), (self.WIN_X, self.WIN_Y / 2, self.WIN_X, self.WIN_Y / 2))

            # Cast rays
            self.cast_rays()

            # Draw map and player
            self.draw_map()
            self.draw_player()

            # Update screen
            pygame.display.flip()

        pygame.display.quit()


if __name__ == "__main__":
    raycaster = Raycaster()
    raycaster.run()
