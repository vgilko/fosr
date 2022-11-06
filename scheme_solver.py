from math import sqrt

from plate import *


def solve(plate: Plate, end_time=100):
    tau = end_time / 100
    time = 0

    print(plate.matrix.shape)

    axis_y_shape = plate.matrix.shape[0]
    axis_x_shape = plate.matrix.shape[1]

    alfa = np.zeros(axis_x_shape)
    beta = np.zeros(axis_x_shape)

    while time < end_time:
        time += tau

        ai = plate.thermal_conductivity / sqrt(plate.dx)
        bi = 2.0 * plate.thermal_conductivity / sqrt(plate.dx) + plate.material_density * plate.heat_capacity / tau
        for j in range(axis_y_shape - 1):
            alfa[1] = 0
            beta[1] = plate.left_border_temperature

            for i in range(1, axis_x_shape):
                ci = plate.thermal_conductivity / sqrt(plate.dx)
                fi = -plate.material_density * plate.heat_capacity * plate.matrix[i][j] / tau
                alfa[i] = ai / (bi - ci * alfa[i - 1])
                beta[i] = (ci * beta[i - 1] - fi) / (bi - ci * alfa[i - 1])

            plate.matrix[axis_x_shape, j] = plate.right_border_temperature

            for i in range(axis_x_shape - 1, 1, -1):
                plate.matrix[i][j] = alfa[i] * plate.matrix[i + 1][j] + beta[i]

        for i in range(1, axis_x_shape):
            alfa[1] = 2.0 * plate.thermal_diffusivity * tau / (2.0 * plate.thermal_diffusivity * tau + sqrt(plate.dy))
            beta[1] = sqrt(plate.dy) * plate.matrix[i][1] / (2.0 * plate.thermal_diffusivity * tau + sqrt(plate.dy))

            for j in range(1, axis_y_shape - 1):
                ai = plate.thermal_conductivity / sqrt(plate.dy)
                bi = 2.0 * plate.thermal_conductivity / sqrt(
                    plate.dy) + plate.material_density * plate.heat_capacity / tau
                ci = plate.thermal_conductivity / sqrt(plate.dy)
                fi = -plate.material_density * plate.heat_capacity * plate.matrix[i][j] / tau

                alfa[j] = ai / (bi - ci * alfa[j - 1])
                beta[j] = (ci * beta[j - 1] - fi) / (bi - ci * alfa[j - 1])

            plate.matrix[i][axis_y_shape] = (2.0 * plate.thermal_diffusivity * tau * beta[axis_y_shape - 1] + sqrt(
                plate.dy) * plate.matrix[i][axis_y_shape]) / (2.0 * plate.thermal_diffusivity * tau *
                                                              (1.0 - alfa[axis_y_shape - 1]) + sqrt(plate.dy))

            for j in range(axis_y_shape - 1, 0, -1):
                plate.matrix[i][j] = alfa[j] * plate.matrix[i][j + 1] + beta[j]


testing_plate = Plate(5, 10, Hole(Point(1, 1), 1, 1), 1, 1)

solve(testing_plate)
