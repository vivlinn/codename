import matplotlib.pyplot as plt
import numpy as np


def visualise(grid):
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    
    # https://stackoverflow.com/questions/24943991/change-grid-interval-and-specify-tick-labels-in-matplotlib
    fig, ax = plt.subplots()
    major_ticks = np.arange(0, 51, 10)
    minor_ticks = np.arange(0, 51, 1)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    # And a corresponding grid
    ax.grid(which='both')
    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)


    for battery in grid.batteries:
        plt.plot(grid.batteries[battery].position_x, grid.batteries[battery].position_y, "r+")

    for house in grid.houses:
        plt.plot(grid.houses[house].position_x, grid.houses[house].position_y, "bo")

    # for cable in grid.cables:
    #     plt.plot(cable.start, cable.end)

    plt.savefig("grid.png")
    plt.show()




