import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def visualise(grid, number):
    plt.grid(b=True, which='major', color='#666666', linestyle='-')

    
    # https://stackoverflow.com/questions/24943991/change-grid-interval-and-specify-tick-labels-in-matplotlib
    fig, ax = plt.subplots()

    major_ticks = np.arange(0, 51, 10)
    minor_ticks = np.arange(0, 51, 1)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)

    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    ax.set_title(f"District {number}")

    # loop through objects to get coordinates
    x_battery = []
    y_battery = []
    for battery in grid.batteries:
        x_battery.append(grid.batteries[battery].position_x)
        y_battery.append(grid.batteries[battery].position_y)

    x_house = []
    y_house = []
    for house in grid.houses:
        x_house.append(grid.houses[house].position_x)
        y_house.append(grid.houses[house].position_y)

    # for cable in grid.cables:
    #     plt.plot(cable.start, cable.end)

    # plot coordinates as simple x's and o's
    ax.plot(x_house, y_house, "rx")
    ax.plot(x_battery, y_battery, "bo")

    # save simple plot with x's and o's
    plt.savefig(f"doc/district_{number}_simple.png")

    # plot coordinates as house and battery images
     # image paths
    house_path = "doc/house.png"
    battery_path = "doc/battery.png"

    house_image = plt.imread(house_path)[10:10+300, 10:10+400]
    battery_image = plt.imread(battery_path)[10:10+600, 10:10+400]

    plot_images(x_house, y_house, house_image, ax=ax)
    plot_images(x_battery, y_battery, battery_image, ax=ax)

    # saves plot with pictures
    plt.savefig(f"doc/district_{number}_image.png")
    plt.show()


def plot_images(x, y, image, ax=None):
    """
    Credits: https://stackoverflow.com/questions/2318288/how-to-use-custom-png-image-marker-with-plot

    This function takes an image and positions it inside annotation boxes using x and y coordinates
    """

    ax = ax or plt.gca()

    for xi, yi in zip(x,y):
        im = OffsetImage(image, zoom=6/ax.figure.dpi)
        im.image.axes = ax

        ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)

        ax.add_artist(ab)





