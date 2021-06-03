import matplotlib.pyplot as plt


def visualise(grid):
    width = grid.get_width()
    height = grid.get_height()
    plt.plot([0, width], [0, height])
    plt.grid(b=True, which='major', color='#666666', linestyle='-')

    for battery in grid.batteries:
        plt.plot(battery.position_x, battery.position_y)

    for house in grid.houses:
        plt.plot(house.position_x, house.position_y)

    for cable in grid.cables:
        plt.plot(cable.start, cable.end)

    plt.show()




