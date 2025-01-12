import math
from geometry import Geometry
from typing import List


class Raycaster:

    def __init__(
        self,
        map_data: List[List[int]],
        field_of_view,
        num_rays,
        speed,
        rotation_speed,
        square_size,
        map_width,
        map_height
    ):
        self.field_of_view: int = field_of_view
        self.num_rays: int = num_rays
        self.speed: int = speed
        self.rotation_speed: int = rotation_speed
        self.square_size: int = square_size
        self.map_width: int = map_width
        self.map_height: int = map_height
        self.map: List[List[int]] = map_data

    def move(self, player_x: float, player_y: float, angle: float) -> tuple[float, float]:
        slope: float = Geometry.calculate_slope_angle(angle)
        x1, y1 = player_x, player_y
        x2, y2 = player_x + 1, player_y + slope
        normalized_angle: float = angle % 360

        # Determine movement direction based on angle
        if 0 <= normalized_angle <= 90 or 270 < normalized_angle <= 360:
            movement_speed = -self.speed
        else:
            movement_speed = self.speed

        # Calculate new position
        y_new: float = y1 + ((y1 - y2) * movement_speed) / (math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
        x_new: float = x1 + ((x1 - x2) * movement_speed) / (math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))

        # Check if the new position is free
        field_value: int = self.map[
            int((self.map_height / self.square_size) - math.floor(y_new / self.square_size))
        ][math.floor(x_new / self.square_size)]

        if field_value == 0:
            return x_new, y_new
        else:
            return x1, y1

    def cast_ray(self, player_x: float, player_y: float, angle: float) -> tuple[float, int, int]:
        normalized_angle: float = angle % 360
        x, y = player_x, player_y
        current_square_x: int = math.floor(x / self.square_size)
        current_square_y: int = math.floor(y / self.square_size)

        # Linear function for the ray
        slope: float = Geometry.calculate_slope_angle(normalized_angle)
        intercept: float = Geometry.calculate_y_intercept(x, y, slope)

        while True:
            # Calculate vertical intersection and the next square
            if 90 <= normalized_angle < 270:
                x_test: float = current_square_x * self.square_size
                next_square_x: int = current_square_x - 1
            else:
                x_test: float = (current_square_x + 1) * self.square_size
                next_square_x: int = current_square_x + 1

            # Calculate horizontal intersection and the next square
            if 180 <= normalized_angle < 360:
                y_test: float = current_square_y * self.square_size
                next_square_y: int = current_square_y - 1
            else:
                y_test: float = (current_square_y + 1) * self.square_size
                next_square_y: int = current_square_y + 1

            # Find the two intersection points
            horizontal_intersection: tuple[float, float] = (Geometry.find_x_value(slope, intercept, y_test), y_test)
            vertical_intersection: tuple[float, float] = (x_test, Geometry.find_y_value(slope, intercept, x_test))

            # Calculate distances to the intersections
            horizontal_distance: float = Geometry.calculate_distance(x, y, horizontal_intersection[0], horizontal_intersection[1])
            vertical_distance: float = Geometry.calculate_distance(x, y, vertical_intersection[0], vertical_intersection[1])

            # Determine which intersection is closer and check for walls
            if horizontal_distance < vertical_distance:
                wall_type: int = self.map[
                    int(((self.map_height / self.square_size) - 1) - next_square_y)
                ][current_square_x]
                if wall_type > 0:
                    return horizontal_distance, 0, wall_type
                else:
                    current_square_y = next_square_y
            else:
                wall_type: int = self.map[
                    int(((self.map_height / self.square_size) - 1) - current_square_y)
                ][next_square_x]
                if wall_type > 0:
                    return vertical_distance, 1, wall_type
                else:
                    current_square_x = next_square_x
