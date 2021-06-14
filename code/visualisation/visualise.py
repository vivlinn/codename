import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def visualise_annealing(state):
    """
    This function takes a state and a district number and creates a visualisation plot using the coordinates of objects.
    """


    x, y = state.plot()
    print(f"x: {x}")
    print(f"y: {y}")
        # x = axis[0]
        # y = axis[1]
        
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.savefig(f"output/annealing.png")

def visualise_grid(grid, number):
    """
    Credits: https://stackoverflow.com/questions/24943991/change-grid-interval-and-specify-tick-labels-in-matplotlib

    This function takes a grid and a district number and creates a visualisation plot using the coordinates of objects.
    """
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    
    # Create a new figure
    fig, ax = plt.subplots()

    # Major ticks every 10, minor ticks every 5
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

    # Get x- and y-coordinates of objects and save in lists
    x_battery = []
    y_battery = []
    for battery in grid.batteries:
        x_battery.append(battery.position_x)
        y_battery.append(battery.position_y)

    x_house = []
    y_house = []
    for house in grid.houses:
        x_house.append(house.position_x)
        y_house.append(house.position_y)
        
        x_route = house.route.list_x
        y_route = house.route.list_y
        ax.plot(x_route, y_route)
                
    
    # test = grid.houses[0]

    # x_route = test.route.list_x
    # y_route = test.route.list_y
    # ax.plot(x_route, y_route)
            
    # for cable in grid.cables:
    #     plt.plot(cable.start, cable.end)

    # Plot coordinates as crosses and dots
    ax.plot(x_house, y_house, "rx")
    ax.plot(x_battery, y_battery, "bo")

    # Save plot with dots and crosses
    plt.savefig(f"output/district_{number}_simple.png")

    # Save images of house and battery in image paths
    house_path = "doc/house.png"
    battery_path = "doc/battery.png"

    house_image = plt.imread(house_path)[10:10+300, 10:10+400]
    battery_image = plt.imread(battery_path)[10:10+600, 10:10+400]

    # Plot coordinates as houses and batteries
    plot_images(x_house, y_house, house_image, ax=ax)
    plot_images(x_battery, y_battery, battery_image, ax=ax)

    # Save plot with houses and batteries
    plt.savefig(f"output/district_{number}_image.png")
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





