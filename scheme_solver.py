from plate import *


class Solver:
    def __init__(self, plate: Plate, laser: Laser, end_time=100):
        self.plate = plate
        self.laser = laser
        self.end_time = end_time

        self.tau = self.end_time / 100

        self.x_axis_shape = plate.matrix.shape[1]
        self.y_axis_shape = plate.matrix.shape[0]

        self.alfa = np.zeros(self.x_axis_shape)
        self.betta = np.zeros(self.x_axis_shape)

        self.a_i_x = plate.thermal_conductivity / (plate.dx ** 2)
        self.b_i_x = 2.0 * self.a_i_x + self.plate.material_density * self.plate.heat_capacity / self.tau
        self.c_i_x = self.a_i_x

        self.tau_coeff = 2.0 * self.plate.thermal_diffusivity * self.tau
        self.dy_sqr = (self.plate.dy ** 2)

        self.a_i_y = plate.thermal_conductivity / self.dy_sqr
        self.b_i_y = 2.0 * self.a_i_y + self.plate.material_density * self.plate.heat_capacity / self.tau
        self.c_i_y = self.a_i_y

        self.fi_coeff = -self.plate.material_density * self.plate.heat_capacity / self.tau

    def solve(self):
        time = 0
        while time < self.end_time:
            time += self.tau

            self.solve_x_axis()
            self.solve_y_axis()

    def solve_y_axis(self):
        for i in range(1, self.x_axis_shape - 2, 1):
            self.alfa[1] = self.tau_coeff / (self.tau_coeff + self.dy_sqr)
            self.betta[1] = self.dy_sqr * self.plate.matrix[1, i] / (self.tau_coeff + self.dy_sqr)

            for j in range(1, self.y_axis_shape - 2, 1):
                if self.plate.is_hole(i + 1, j + 1):
                    continue

                f_i = self.fi_coeff * self.plate.matrix[j, i]

                j_coeff = self.b_i_x - self.c_i_x * self.alfa[j - 1]
                self.alfa[j] = self.a_i_x / j_coeff
                self.betta[j] = (self.c_i_x * self.betta[j - 1] - f_i) / j_coeff

            last_y_index = self.y_axis_shape - 1
            self.plate.matrix[last_y_index, i] = \
                (self.tau_coeff * self.betta[last_y_index] + self.dy_sqr * self.plate.matrix[
                    last_y_index, i]) / (self.tau_coeff * (1.0 - self.alfa[last_y_index]) + self.dy_sqr)

            for j in range(last_y_index - 1, 0, -1):
                if not self.plate.is_hole(i + 1, j + 1):
                    self.plate.matrix[j, i] = self.alfa[j] * self.plate.matrix[j + 1, i] + self.betta[
                        j] + self.laser.calculate(self.plate.x[i], self.plate.y[j])

    def solve_x_axis(self):
        self.alfa[1] = 0
        self.betta[1] = self.plate.outer_border_temperature

        for j in range(self.y_axis_shape - 1):
            for k in range(1, self.x_axis_shape - 1, 1):
                if not (self.plate.is_hole(k + 2, j + 2) or self.plate.is_hole(k, j)):
                    f_i = self.fi_coeff * self.plate.matrix[j, k]

                    k_coeff = self.b_i_x - self.c_i_x * self.alfa[k - 1]
                    self.alfa[k] = self.a_i_x / k_coeff
                    self.betta[k] = (self.c_i_x * self.betta[k - 1] - f_i) / k_coeff

            self.plate.matrix[j, self.x_axis_shape - 1] = self.plate.outer_border_temperature

            for k in range(self.x_axis_shape - 2, 0, -1):
                if not (self.plate.is_hole(k + 2, j + 2) or self.plate.is_hole(k, j)):
                    self.plate.matrix[j, k] = self.alfa[k] * self.plate.matrix[j, k + 1] + self.betta[
                        k] + self.laser.calculate(self.plate.x[k], self.plate.y[j])

    if __name__ == '__main__':
        pass
