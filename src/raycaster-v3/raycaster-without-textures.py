import math
import pygame
from typing import List

pygame.init()

class Raycaster:
    def __init__(self) -> None:
        self.map: List[List[int]] = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.WIN_X = 700
        self.WIN_Y = 650
        self.screen = pygame.display.set_mode((self.WIN_X, self.WIN_Y))
        pygame.display.set_caption("Raycaster by Pascal and Yannick")
        self.pLogo = pygame.image.load("images/logo.png")
        pygame.display.set_icon(self.pLogo)

        self.floor_image = pygame.image.load("images/floor.png").convert_alpha()
        self.floor = pygame.transform.scale(self.floor_image, (self.WIN_X, int(self.WIN_Y / 2)))
        self.sky_image = pygame.image.load("images/sky.png").convert_alpha()
        self.sky = pygame.transform.scale(self.sky_image, (self.WIN_X, int(self.WIN_Y / 2)))

        self.PI = math.pi
        self.MAX_FPS = 60
        self.MOVE_SPEED = 0.06
        self.ROTATE_SPEED = math.radians(1.3)
        self.LINE_WIDTH = 2
        self.NUM_RAYS = int(self.WIN_X / self.LINE_WIDTH) + 1
        self.FIELD_OF_VIEW = math.radians(50)
        self.RAY_DENSITY = self.FIELD_OF_VIEW / (self.NUM_RAYS - 1)
        self.SIZE = 800
        self.LIGHTNESS = 1000
        self.SHADOW = 2.5

        self.player_x = 7.01
        self.player_y = 3.01
        self.direction = math.radians(270.01)

    def run(self) -> None:
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(100)
            fps = clock.get_fps()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.move_forward()
            if keys[pygame.K_DOWN]:
                self.move_backward()
            if keys[pygame.K_RIGHT]:
                self.turn_right()
            if keys[pygame.K_LEFT]:
                self.turn_left()

            self.screen.fill((25, 25, 25))
            self.screen.blit(self.sky, (0, 0))
            self.screen.blit(self.floor, (0, self.WIN_Y / 2))

            self.draw_rays()

            pygame.display.flip()

        pygame.display.quit()

    def move_forward(self) -> None:
        sin_direction = math.sin(self.direction)
        cos_direction = math.cos(self.direction)
        if not self.map[int(self.player_y)][int(self.player_x + self.MOVE_SPEED * cos_direction)]:
            self.player_x += self.MOVE_SPEED * cos_direction
        if not self.map[int(self.player_y - self.MOVE_SPEED * sin_direction)][int(self.player_x)]:
            self.player_y -= self.MOVE_SPEED * sin_direction

    def move_backward(self) -> None:
        sin_direction = math.sin(self.direction)
        cos_direction = math.cos(self.direction)
        if not self.map[int(self.player_y)][int(self.player_x - self.MOVE_SPEED * cos_direction)]:
            self.player_x -= self.MOVE_SPEED * cos_direction
        if not self.map[int(self.player_y + self.MOVE_SPEED * sin_direction)][int(self.player_x)]:
            self.player_y += self.MOVE_SPEED * sin_direction

    def turn_right(self) -> None:
        self.direction += self.ROTATE_SPEED
        self.direction %= 2 * self.PI

    def turn_left(self) -> None:
        self.direction -= self.ROTATE_SPEED
        self.direction %= 2 * self.PI

    def draw_rays(self) -> None:
        ray_direction = self.direction - self.FIELD_OF_VIEW / 2
        for col in range(self.NUM_RAYS):
            ray_block_x = int(self.player_x)
            ray_block_y = int(self.player_y)

            direction_deg = math.degrees(ray_direction) % 360
            if direction_deg > 0 and direction_deg < 180:
                horizontal_x = self.player_x + (self.player_y % 1) / math.tan(ray_direction)
                delta_x = 1 / math.tan(ray_direction)
                vz_y = -1
            else:
                horizontal_x = self.player_x + (self.player_y % 1 - 1) / math.tan(ray_direction)
                delta_x = -1 / math.tan(ray_direction)
                vz_y = 1

            if direction_deg > 270 or direction_deg < 90:
                vertical_x = math.ceil(self.player_x)
                vz_x = 1
            else:
                vertical_x = math.floor(self.player_x)
                vz_x = -1

            wall = False
            while not wall:
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

                if self.map[ray_block_y][ray_block_x]:
                    texture = self.map[ray_block_y][ray_block_x]
                    wall = True

            ray_length = (intersection_x - self.player_x) / math.cos(ray_direction)
            distance = ray_length * math.cos(ray_direction - self.direction)

            line_height = self.SIZE / distance
            draw_start = (self.WIN_Y / 2) - (line_height / 2)
            if draw_start < 0:
                draw_start = 0
            draw_end = (self.WIN_Y / 2) + (line_height / 2)
            if draw_end > self.WIN_Y:
                draw_end = self.WIN_Y

            light = int(self.LIGHTNESS / distance)
            if light > 255:
                light = 255

            if side:
                light /= self.SHADOW

            color = (0, light, 0)
            pygame.draw.line(self.screen, color, (col * self.LINE_WIDTH, draw_start),
                             (col * self.LINE_WIDTH, draw_end), self.LINE_WIDTH)

            ray_direction += self.RAY_DENSITY

if __name__ == "__main__":
    raycaster = Raycaster()
    raycaster.run()
