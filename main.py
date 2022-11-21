import matplotlib.pyplot as plt

from scheme_solver import *


def make_plot(plate: Plate):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y = np.meshgrid(plate.x, plate.y)
    ax.plot_surface(X, Y, plate.matrix, rstride=1, cstride=1, cmap='viridis')
    plt.show()


def main():
    plate = Plate(10, 10, Hole(Point(4, 4), 3, 3), 0.2, 0.2)

    Solver(plate, Laser(1, 1)).solve()

    make_plot(plate)


if __name__ == '__main__':
    main()
