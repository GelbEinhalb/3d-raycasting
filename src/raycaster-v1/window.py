import pygame
import math
from raycaster import Raycaster

from typing import List
from typing import Union

MAP: List[List[int]] = [
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,1,0,0,0,2,3,0,0,0,4,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,5,0,0,0,0,0,7,0,0,0,6,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
]

class Window:
    def __init__(self):
        pygame.init()

        # Screen settings
        self.screen_width: int = 600
        self.screen_height: int = 600
        self.screen: pygame.Surface = pygame.display.set_mode([self.screen_width, self.screen_height])
        pygame.display.set_caption("Raycaster")

        # Map settings
        self.map_width: int = 1000
        self.map_height: int = 1000
        self.square_size: int = 50
        self.fov: int = 35
        self.ray_density: float = 0.1
        self.num_rays: int = int(self.fov / self.ray_density + 1)
        self.line_width: float = self.screen_width / self.num_rays

        # Player settings
        self.player_x: float = 200
        self.player_y: float = 200
        self.direction: float = 90.1
        self.move_speed: int = 4
        self.turn_speed: int = 1

        # Load textures
        self.floor_texture: pygame.Surface = pygame.transform.scale(pygame.image.load("images/floor.png"), (600, 300))
        self.sky_texture: pygame.Surface = pygame.transform.scale(pygame.image.load("images/sky.png"), (600, 300))

        # Initialize Raycaster
        self.raycaster: Raycaster = Raycaster(
            map_data=MAP,
            field_of_view=self.fov,
            num_rays=self.num_rays,
            speed=self.move_speed,
            rotation_speed=self.turn_speed,
            square_size=self.square_size,
            map_width=self.map_width,
            map_height=self.map_height
        )

        # Clock for controlling FPS
        self.clock = pygame.time.Clock()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction -= self.turn_speed
        if keys[pygame.K_LEFT]:
            self.direction += self.turn_speed
        if keys[pygame.K_UP]:
            self.player_x, self.player_y = self.raycaster.move(self.player_x, self.player_y, self.direction)
        if keys[pygame.K_DOWN]:
            self.player_x, self.player_y = self.raycaster.move(self.player_x, self.player_y, self.direction - 180)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.floor_texture, (0, 300))
        self.screen.blit(self.sky_texture, (0, 0))

        ray_info: List[List[Union[int, float]]] = []
        angle: float = self.fov / 2
        for _ in range(self.num_rays):
            distance, vertical, wall_type = self.raycaster.cast_ray(self.player_x, self.player_y, self.direction + angle)
            ray_info.append([math.cos(math.radians(angle)) * distance, vertical, wall_type])
            angle -= self.ray_density

        for i, info in enumerate(ray_info):
            brightness: float = 40_000 / info[0]
            brightness: float = min(brightness, 255)
            if info[1]:
                brightness /= 2

            color = {
                1: (brightness, 0, 0),
                2: (0, brightness, 0),
                3: (0, 0, brightness),
                4: (brightness, brightness, 0),
                5: (0, brightness, brightness),
                6: (brightness, 0, brightness),
            }.get(info[2], (brightness, brightness, brightness))

            rect_height: float = 100_000 / info[0]
            pygame.draw.rect(
                self.screen,
                color,
                (
                    i * self.screen_width / len(ray_info),
                    300 - rect_height / 2,
                    self.screen_width / len(ray_info) + 1,
                    rect_height,
                ),
            )

        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.handle_input()
            self.render()


if __name__ == "__main__":
    Window().run()
