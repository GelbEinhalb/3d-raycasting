"""
this is a 2D test
"""

import pygame
import math
import numpy as np

class Player:
    def __init__(self, x_pos: float, y_pos: float, direction: float, walking_speed: float, spinning_speed: float) -> None:
        self.x_pos: float = x_pos
        self.y_pos: float = y_pos
        self.direction: float = direction
        self.slope: float = math.tan(math.radians(self.direction))
        self.WALKING_SPEED: float = walking_speed
        self.SPINNING_SPEED: float = spinning_speed

    def walk(self, up_pressed: bool, down_pressed: bool) -> None:
        if up_pressed and not down_pressed:
            self.x_pos += self.WALKING_SPEED * math.cos(math.radians(self.direction))
            self.y_pos += self.WALKING_SPEED * math.sin(math.radians(self.direction))
            if self.wall_touched():
                self.x_pos -= self.WALKING_SPEED * math.cos(math.radians(self.direction))
                self.y_pos -= self.WALKING_SPEED * math.sin(math.radians(self.direction))

        if down_pressed and not up_pressed:
            self.x_pos -= self.WALKING_SPEED * math.cos(math.radians(self.direction))
            self.y_pos -= self.WALKING_SPEED * math.sin(math.radians(self.direction))
            if self.wall_touched():
                self.x_pos += self.WALKING_SPEED * math.cos(math.radians(self.direction))
                self.y_pos += self.WALKING_SPEED * math.sin(math.radians(self.direction))

    def spin(self, right_pressed: bool, left_pressed: bool) -> None:
        if right_pressed and not left_pressed:
            self.direction -= self.SPINNING_SPEED
            self.slope = math.tan(math.radians(self.direction))

        if left_pressed and not right_pressed:
            self.direction += self.SPINNING_SPEED
            self.slope = math.tan(math.radians(self.direction))

    def wall_touched(self) -> bool:
        square_val, _, _ = map_object.pos_square(self.x_pos, self.y_pos)
        return square_val >= 1

    def get_pos(self) -> tuple[float, float]:
        return self.x_pos, self.y_pos

class Map:
    def __init__(self, map_array: np.ndarray, cube_size: int) -> None:
        self.map_array: np.ndarray = map_array
        self.cube_size: int = cube_size
        self.map_shape: int = map_array.shape[0]
        self.map_size: int = self.map_shape * cube_size
        self.map_screen_ratio: float = self.map_size / WIN_X
        self.square_size: float = WIN_X / self.map_shape

    def pos_square(self, x: float, y: float) -> tuple[int, int, int]:
        square_x: int = int(x // self.cube_size)
        square_y: int = int(self.map_shape - y // self.cube_size - 1)
        square_val: int = self.map_array[square_y, square_x]
        return square_val, square_x, square_y

    def draw_2d(self) -> None:
        screen.fill((0, 0, 0))

        for y in range(self.map_shape):
            for x in range(self.map_shape):
                color: tuple[int, int, int] = (0, 0, 255) if self.map_array[y, x] == 1 else (0, 0, 0)
                pygame.draw.rect(screen, color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size))

        player_x, player_y = player.get_pos()
        player_x /= self.map_screen_ratio
        player_y = WIN_Y - (player_y / self.map_screen_ratio)
        pygame.draw.rect(screen, (255, 255, 255), (player_x - 5, player_y - 5, 10, 10))

        pygame.display.flip()

# Constants
WIN_X: int = 600
WIN_Y: int = 600

# Pygame initialization
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((WIN_X, WIN_Y))
pygame.display.set_caption("Raycaster 2.0")

# Map and player initialization
map_array: np.ndarray = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
])

player: Player = Player(500, 500, 45, 3, 3)
map_object: Map = Map(map_array, 50)


if __name__ == "__main__":
    clock: pygame.time.Clock = pygame.time.Clock()
    run: bool = True

    while run:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        player.walk(keys[pygame.K_UP], keys[pygame.K_DOWN])
        player.spin(keys[pygame.K_RIGHT], keys[pygame.K_LEFT])
        map_object.draw_2d()

    pygame.quit()
