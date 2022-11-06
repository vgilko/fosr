import numpy as np


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Hole:
    def __init__(self, start: Point, height: float, width: float):
        self.__start = start
        self.__height = height
        self.__width = width

    def get_start_x(self):
        return self.__start.x

    def get_start_y(self):
        return self.__start.y

    def get_end_x(self):
        return self.__start.x + self.__width - 1

    def get_end_y(self):
        return self.__start.y + self.__height - 1


class Plate:
    def __init__(self,
                 height: float,
                 width: float,
                 hole: Hole,
                 dx=0.5,
                 dy=0.5,
                 start_temperature=1273,
                 left_border_temperature=1900,
                 right_border_temperature=1900,
                 thermal_conductivity=60,
                 material_density=3070,
                 heat_capacity=1260):
        self.thermal_conductivity = thermal_conductivity
        self.material_density = material_density
        self.heat_capacity = heat_capacity
        self.left_border_temperature = left_border_temperature
        self.right_border_temperature = right_border_temperature
        self.thermal_diffusivity = self.thermal_conductivity / (material_density * heat_capacity)
        self.dx = dx
        self.dy = dy
        self.hole = hole

        self.hole_y_idx = -1

        self.__build_axis(dx, dy, height, width)

        self.__build_matrix()

        self.__set_temperature(start_temperature)

    def __build_axis(self, dx, dy, height, width):
        self.y = np.arange(0, height + dy / 1000, dy)
        self.x = np.arange(0, width + dx / 1000, dx)

    def __build_matrix(self):
        shape_y = self.y.shape[0]
        shape_x = self.x.shape[0]
        amount = shape_y * shape_x

        temp_array = np.zeros(amount, float)
        self.matrix = temp_array.reshape(shape_y, shape_x)

    def make_hole(self):
        if self.hole is not None:
            hole_start_y = self.hole.get_start_y()
            hole_start_x = self.hole.get_start_x()

            hole_end_x = self.hole.get_end_x()
            hole_end_y = self.hole.get_end_y()

            for idx_y, value_y in enumerate(self.y):
                is_hole = hole_start_y <= value_y <= hole_end_y
                for idx_x, value_x in enumerate(self.x):
                    if hole_start_x <= value_x <= hole_end_x and is_hole:
                        self.matrix[idx_x, idx_y] = np.NaN

    def __set_temperature(self, temperature):
        self.matrix[~np.isnan(self.matrix)] = temperature
