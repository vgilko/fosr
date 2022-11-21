from cmath import exp

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


class Laser:
    def __init__(self, x, y, b=1.2, f0=30):
        self.x = x
        self.y = y
        self.b = b
        self.f0 = f0

    def calculate(self, x, y):
        return self.f0 * exp(-self.b * ((x - self.x) ** 2) * ((y - self.y) ** 2))


class Plate:
    def __init__(self,
                 height: float,
                 width: float,
                 hole: Hole,
                 dx=0.5,
                 dy=0.5,
                 start_temperature=1373,
                 outer_border_temperature=1300,
                 internal_border_temperature=1300,
                 thermal_conductivity=60,   # теплопроводность
                 material_density=3070,     # плотность пластины
                 heat_capacity=1260):       # теплоемкость
        self.thermal_conductivity = thermal_conductivity
        self.material_density = material_density
        self.heat_capacity = heat_capacity
        self.outer_border_temperature = outer_border_temperature
        self.internal_border_temperature = internal_border_temperature
        self.thermal_diffusivity = self.thermal_conductivity / (material_density * heat_capacity)   # температуропроводность
        self.dx = dx
        self.dy = dy
        self.hole = hole

        self.hole_x_idx = -1
        self.hole_y_idx = -1
        self.hole_x_end_idx = -1
        self.hole_y_end_idx = -1

        self.__build_axis(dx, dy, height, width)

        self.__build_matrix()

        self.__set_up_hole_indexes()

        self.make_hole()

        self.__set_temperature(start_temperature)
        self.__set_temperature_internal_border(internal_border_temperature)
        self.__set_temperature_outer_border(outer_border_temperature)

    def __build_axis(self, dx, dy, height, width):
        self.y = np.arange(0, height, dy)
        self.x = np.arange(0, width, dx)

    def __build_matrix(self):
        shape_y = self.y.shape[0]
        shape_x = self.x.shape[0]
        amount = shape_y * shape_x

        temp_array = np.zeros(amount, float)
        self.matrix = temp_array.reshape(shape_y, shape_x)

    def __set_up_hole_indexes(self):
        hole_start_y = self.hole.get_start_y()
        hole_start_x = self.hole.get_start_x()

        hole_end_x = self.hole.get_end_x()
        hole_end_y = self.hole.get_end_y()

        for idx_y, value_y in enumerate(self.y):
            if value_y >= hole_start_y:
                self.hole_y_idx = idx_y
                break

        for idx_y, value_y in reversed(list(enumerate(self.y))):
            if value_y <= hole_end_y:
                self.hole_y_end_idx = idx_y
                break

        for idx_x, value_x in enumerate(self.x):
            if value_x >= hole_start_x:
                self.hole_x_idx = idx_x
                break

        for idx_x, value_x in reversed(list(enumerate(self.x))):
            if value_x <= hole_end_x:
                self.hole_x_end_idx = idx_x
                break

    def make_hole(self):
        if self.hole is not None:
            for x in range(self.hole_x_idx, self.hole_x_end_idx + 1, 1):
                for y in range(self.hole_y_idx, self.hole_y_end_idx + 1, 1):
                    self.matrix[x, y] = np.NaN

    def __set_temperature(self, temperature):
        self.matrix[~np.isnan(self.matrix)] = temperature

    def __set_temperature_internal_border(self, temperature):
        for x in range(self.hole_x_idx - 1, self.hole_x_end_idx + 2, 1):
            self.matrix[x, self.hole_y_idx - 1] = temperature
            self.matrix[x, self.hole_y_end_idx + 1] = temperature
        for y in range(self.hole_y_idx, self.hole_y_end_idx + 1, 1):
            self.matrix[self.hole_x_idx - 1, y] = temperature
            self.matrix[self.hole_x_end_idx + 1, y] = temperature

    def __set_temperature_outer_border(self, temperature):
        y_shape = self.matrix.shape[0]
        x_shape = self.matrix.shape[1]

        for x in range(x_shape):
            self.matrix[0, x] = temperature
            self.matrix[y_shape - 1, x] = temperature
        for y in range(y_shape):
            self.matrix[y, 0] = temperature
            self.matrix[y, x_shape - 1] = temperature

    def is_hole(self, i: int, j: int):
        return self.is_x_in_hole(i) and self.is_y_in_hole(j)

    def is_x_in_hole(self, idx: int):
        return self.hole_x_idx < idx < self.hole_x_end_idx

    def is_y_in_hole(self, idx: int):
        return self.hole_y_idx < idx < self.hole_y_end_idx
