import math

class Geometry:

    @staticmethod
    def calculate_slope_angle(degree: float) -> float:
        angle: float = math.tan(math.radians(degree))
        return angle

    @staticmethod
    def calculate_y_intercept(x: float, y: float, slope: float) -> float:
        x2: float = x + 1
        y2: float = y + slope
        slope: float = (y - y2) / (x - x2)
        y_intercept: float = -slope * x + y
        return y_intercept

    @staticmethod
    def calculate_x_intercept(x: float, y: float, slope: float) -> float:
        x2: float = x + 1
        y2: float = y + slope
        slope: float = (y - y2) / (x - x2)
        y_intercept: float = -slope * x + y
        x_intercept: float = -(1 / slope) * y_intercept
        return x_intercept

    @staticmethod
    def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        distance: float = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance

    @staticmethod
    def calculate_midpoint(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
        midpoint_x: float = x1 + (x2 - x1) / 2
        midpoint_y: float = y1 + (y2 - y1) / 2
        return midpoint_x, midpoint_y

    @staticmethod
    def calculate_slope(x1: float, y1: float, x2: float, y2: float) -> float:
        if x1 == x2:
            return float('inf')  # Infinite slope for vertical lines
        slope: float = (y2 - y1) / (x2 - x1)
        return slope

    @staticmethod
    def calculate_y_intercept_from_points(x1: float, y1: float, x2: float, y2: float) -> float:
        if x1 == x2:
            return float('inf')  # Undefined y-intercept for vertical lines
        slope: float = (y2 - y1) / (x2 - x1)
        y_intercept: float = -slope * x1 + y1
        return y_intercept

    @staticmethod
    def calculate_x_intercept_from_points(x1: float, y1: float, x2: float, y2: float) -> float:
        if x1 == x2:
            return x1  # Vertical line, x-intercept is x1
        slope: float = (y2 - y1) / (x2 - x1)
        y_intercept: float = -slope * x1 + y1
        x_intercept: float = -(1 / slope) * y_intercept
        return x_intercept

    @staticmethod
    def find_y_value(slope: float, y_intercept: float, x: float) -> float:
        if slope == 0:
            slope = 0.0001  # Avoid division by zero
        y_value: float = slope * x + y_intercept
        return y_value

    @staticmethod
    def find_x_value(slope: float, y_intercept: float, y: float) -> float:
        if slope == 0:
            slope = 0.0001  # Avoid division by zero
        x_value: float = (y - y_intercept) / slope
        return x_value
