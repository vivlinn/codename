from code.classes.route import Route

def better_cables(grid):
    """
    This function tries to assign the closest battery for every house.
    It then checks if battery capacity is not exceeded, else assigns another battery to the house.
    Then adds all route coordinates to a route class for every house
    
    grid: Grid class

    Returns: None
    """

    sorted_output = bubbleSort(grid.houses, "house")

    # loop through all houses in grid
    for house in sorted_output:

        # assign closest battery to house
        assign_battery(grid, house)

    houses_left = remove_excessive_houses()

    bubbleSort(houses_left, "house")
    sorted_batteries = bubbleSort(grid.batteries, "battery")

    rearrange_houses(houses_left, sorted_batteries)
    
    for house in grid.houses:
        horizontal, vertical = define_direction(house)

        lay_cables(grid, house, horizontal, vertical)

def rearrange_houses(houses_left, sorted_batteries):
    """
    takes all the houses without battery and tries to append them to a battery if possible
    
    houses_left: list
    sorted_batteries: list

    Returns: None
    """

    # go until no more houses left
    while len(houses_left) > 0:

       # go till battery isn't too full
        for house in houses_left:
        
             # iterate over batteries
            for battery in sorted_batteries:

                # if battery has enough capacity for this house
                if house.max_output <= battery.remaining:
                    
                    # connect house to battery
                    house.route = Route(battery, house.position_x, house.position_y)
                    battery.add_house(house)
                    
                    # update remaining capacity
                    battery.update_remaining(house, "subtract")
                   
                    # remove house from list
                    houses_left.remove(house)
                    break   

def remove_excessive_houses(grid):
    """
    unconnects houses from battery and appends these left over houses to a list
    
    grid: Grid class

    Returns: list
    """

    houses_left = []

    # iterate over batteries
    for battery in grid.batteries:
            
        # if battery is full
        while battery.remaining < 0:

            # remove last house
            house = battery.remove_house()

            # update houses left
            houses_left.append(house)

            house.check = True

            # update remainig capacity of battery
            battery.update_remaining(house, "add")
            
        return houses_left

def define_direction(house):
    """
    Get direction for path for x-axis and y-axis by checking the differnce between house and battery coordinates
    
    house: House class

    Returns: horizontal: int, vertical: int
    """
    # if house is further on x-axis than battery: decrease x-coordinate
    if house.route.list_x[-1] >= house.route.battery.position_x:
        horizontal = - 1
    # else increase x-coordinate
    else:
        horizontal = 1

    # if house is further on y-axis than battery: decrease y-coordinate
    if house.route.list_y[-1] > house.route.battery.position_y:
        vertical = -1
    # else increase y-coordinate
    else:
        vertical = 1

    return horizontal, vertical


def assign_battery(grid, house):
    """
    assigns a battery to a house with the least distance between them

    grid: Grid class;
    house: House class

    Returns: None
    """

    # initiate variable to save coupled battery
    battery_chosen = None

    # save shortest distance in best, start with longest possible
    best = grid.grid_height + grid.grid_width + 2

    # loop through batteries
    for battery in grid.batteries:

        # calculate distance between x-coordinates + distance between y-coordinates from house to battery
        distance = abs(battery.position_x - house.position_x) + abs(battery.position_y - house.position_y)

        # if this is shorter than for last battery:
        if distance < best:

            # update best to shorter distance
            best = distance

            # set this battery as coupled battery
            battery_chosen = battery
    
    # Create Route class for house/battery couple
    house.route = Route(battery_chosen, house.position_x, house.position_y)

    # append house to list of connected houses for battery       
    battery_chosen.add_house(house)

    # update remaining capacity for battery
    battery_chosen.update_remaining(house, "subtract")

    return

# https://www.programiz.com/python-programming/methods/list/sort
def bubbleSort(arr, object):
    """
    sorts a list using bubble sort

    arr: list

    Returns: list
    """

    n = len(arr)

    # Traverse through all array elements
    for i in range(n-1):

        # Last i elements are already in place
        for j in range(0, n-i-1):

            # Swap if the element found is greater
            if object == "house":
                if arr[j].max_output < arr[j + 1].max_output :
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            else:
                if arr[j].remaining > arr[j + 1].remaining :
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr
    

def lay_cables(grid, house, horizontal, vertical):
    """
    Lays cables from house to battery and adds the coordinates to route class.
    Starts by going horizontal, then vertical until battery is reached.

    grid: Grid class; 
    house: House class; 
    horizontal: int; 
    vertical: int

    Returns: None
    """

    # save non-chosen batteries in list
    other_batteries = []
    for battery in grid.batteries:
        if battery != house.route.battery:
            other_batteries.append(battery)

    # loop till x-coordinate of cable matches x-coordinate of battery
    while house.route.list_x[-1] != house.route.battery.position_x:

        # when house is not coupled to closest battery
        if house.check == True:
            axis = "x"

            # check if path doesn't cross other batteries
            bypass_battery(house, horizontal, vertical, axis, other_batteries)

            # re-calculate direction from path to battery
            horizontal, vertical = define_direction(house)
        else:
            house.route.list_x.append(house.route.list_x[-1] + horizontal)
            house.route.list_y.append(house.route.list_y[-1])

    # loop till y-coordinate of cable matches y-coordinate of battery
    while house.route.list_y[-1] != house.route.battery.position_y:
        
        # when house is not coupled to closest battery
        if house.check == True:
            axis = "y"

            # check if path doesn't cross other batteries
            bypass_battery(house, horizontal, vertical, axis, other_batteries)

            # re-calculate direction from path to battery
            horizontal, vertical = define_direction(house)
        else:
            house.route.list_y.append(house.route.list_y[-1] + vertical)
            house.route.list_x.append(house.route.list_x[-1])

    return

def bypass_battery(house, horizontal, vertical, axis, other_batteries):
    """
    bypasses battery if house is relocated and needed

    grid: Grid class; 
    house: House class; 
    x: int;
    y: int;
    horizontal: int; 
    vertical: int;
    axis: string

    returns: None
    """
    x = house.route.list_x[-1]
    y = house.route.list_x[-1]
    
    # check if new coordinated don't lead to other batteries
    for battery in other_batteries:
            
        # if path is moving across the x-axis
        if axis == "x":

            # bypass other batteries 
            if x + horizontal == battery.position_x and y == battery.position_y:

                # Move one y-coordinate up or down, then one x coordinate left or right depending on direction towards right battery
                house.route.list_y.extend([y + vertical, y + vertical])
                house.route.list_x.extend([x, x + horizontal])
            
        # bewegen over de y-as
        else:

            # bypass other batteries 
            if x == battery.position_x and y + vertical == battery.position_y:

                # Move one x coordinate left or right, then one y-coordinate up or down depending on direction towards right battery
                house.route.list_x.extend([x + horizontal, x + horizontal])
                house.route.list_y.extend([y, y + vertical])

        return

    # append if bypasses is not needed
    if axis == "x":

        # changes x coordinate
        house.route.list_x.append(x + horizontal)
        house.route.list_y.append(y)
    else:

        # changes y coordinate
        house.route.list_x.append(x)
        house.route.list_y.append(y + vertical)

    return