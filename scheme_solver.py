from math import sqrt

import matplotlib.pyplot as plt

from plate import *


def solve(plate: Plate, end_time=1000):
    tau = end_time / 100

    axis_y_shape = plate.matrix.shape[0]
    axis_x_shape = plate.matrix.shape[1]

    alfa = np.zeros(axis_x_shape)
    beta = np.zeros(axis_x_shape)

    time = 0

    sqrt_dy = sqrt(plate.dy)
    ci = plate.thermal_conductivity / sqrt(plate.dx)
    atau_coeff = 2.0 * plate.thermal_diffusivity * tau
    thermal_conductivity_sqrt = plate.thermal_conductivity / sqrt_dy

    while time < end_time:
        time += tau

        # ai = plate.thermal_conductivity / sqrt(plate.dx)
        bi = 2.0 * ci + plate.material_density * plate.heat_capacity / tau
        for j in range(axis_y_shape):
            alfa[1] = 0
            beta[1] = plate.left_border_temperature

            for i in range(1, axis_x_shape):
                fi = -plate.material_density * plate.heat_capacity * plate.matrix[j][i] / tau
                alfa[i] = ci / (bi - ci * alfa[i - 1])
                beta[i] = (ci * beta[i - 1] - fi) / (bi - ci * alfa[i - 1])

            plate.matrix[j][axis_x_shape - 1] = plate.right_border_temperature

            for i in range(axis_x_shape - 2, 1, -1):
                plate.matrix[j][i] = alfa[i] * plate.matrix[j][i + 1] + beta[i]

        for i in range(1, axis_x_shape - 1):
            alfa[1] = atau_coeff / (atau_coeff + sqrt_dy)
            beta[1] = sqrt_dy * plate.matrix[1][i] / (atau_coeff + sqrt_dy)

            for j in range(1, axis_y_shape):
                ai = thermal_conductivity_sqrt
                bi = 2.0 * thermal_conductivity_sqrt + plate.material_density * plate.heat_capacity / tau
                ci = thermal_conductivity_sqrt
                fi = -plate.material_density * plate.heat_capacity * plate.matrix[j][i] / tau

                alfa[j] = ai / (bi - ci * alfa[j - 1])
                beta[j] = (ci * beta[j - 1] - fi) / (bi - ci * alfa[j - 1])

            plate.matrix[axis_y_shape - 1][i] = (atau_coeff * beta[axis_y_shape - 2] +
                                                 sqrt_dy * plate.matrix[axis_y_shape - 1][i]) / \
                                                (atau_coeff * (1.0 - alfa[axis_y_shape - 2]) + sqrt_dy)

            for j in range(axis_y_shape - 2, 0, -1):
                plate.matrix[j][i] = alfa[j] * plate.matrix[j + 1][i] + beta[j]


testing_plate = Plate(10, 10, Hole(Point(4, 4), 4, 4), 0.2, 0.2)

solve(testing_plate)

testing_plate.make_hole()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
X, Y = np.meshgrid(testing_plate.x, testing_plate.y)
ax.plot_surface(X, Y, testing_plate.matrix, rstride=1, cstride=1, cmap='viridis')

plt.show()
