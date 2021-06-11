import random
from code.classes.route import Route
import queue
import copy

def better_cables(grid):

    sorted_output = bubbleSort(grid.houses)

    # loop through all houses in grid
    for house in sorted_output:

        # assign closest battery to house
        assign_battery(grid, house)

    houses_left = []

    # iterate over batteries
    for battery in grid.batteries:
            
        # if battery is full
        while battery.remaining < 0:
            # remove last house
            house = battery.connected_houses.pop()
            # update houses left
            houses_left.append(house)
            house.check = True
            # update remainig capacity of battery
            battery.remaining += house.max_output

    bubbleSort(houses_left)

    # go until no more houses left
    while len(houses_left) > 0:
        print()
        print(len(houses_left))
        

        # iterate over batteries
        for battery in grid.batteries:
            print()
            print(battery.remaining)
            
            # go till battery isn't too full
            for house in houses_left:
                print()
                print(house.max_output)


            

                # if battery has enough capacity for this house
                if house.max_output <= battery.remaining:
                    # connect house to battery
                    house.route = Route(battery, house.position_x, house.position_y)
                    battery.connected_houses.append(house)
                    # update remaining capacity
                    battery.remaining -= house.max_output
                    # remove house from list
                    houses_left.remove(house)
                    break

    for house in grid.houses:
        if house.position_x >= house.route.battery.position_x:
            horizontal = -1
        else:
            horizontal = 1
        
        if house.position_y > house.route.battery.position_y:
            vertical = -1
        else:
            vertical = 1
        
        lay_cables(grid, house, horizontal, vertical)

        




def assign_battery(grid, house):
    """
    assigns a battery to a house with the least distance between them
    Input: grid class, house class
    Returns: None
    """
    battery_chosen = None

    best = grid.grid_height + grid.grid_width + 2
    for battery in grid.batteries:
        distance = abs(battery.position_x - house.position_x) + abs(battery.position_y - house.position_y)
        if distance < best:
            best = distance
            battery_chosen = battery
    
    # add battery to Route
    house.route = Route(battery_chosen, house.position_x, house.position_y)
    # append house to list of connected houses for battery       
    battery_chosen.connected_houses.append(house)

    # update remaining capacity for battery
    battery_chosen.remaining -= house.max_output

    return

# https://www.programiz.com/python-programming/methods/list/sort
def bubbleSort(arr):
    """
    sorts a list using bubble sort
    Input: list
    Returns: list
    """
    n = len(arr)

    # Traverse through all array elements
    for i in range(n-1):

        # Last i elements are already in place
        for j in range(0, n-i-1):

            # Swap if the element found is greater
            if arr[j].max_output < arr[j + 1].max_output :
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr

        

def lay_cables(grid, house, horizontal, vertical):
    """
    lays cables from house to battery and adds them to route.list
    Input: grid class, house class, horizontal integer, vertical integer
    returns: none
    """
    while house.route.list_x[-1] != house.route.battery.position_x:
        print("laatste van lijst: ")
        print(house.route.list_x[-1])
        print("batterij x: ")
        print(house.route.battery.position_x)

        if house.check == True:
            axis = "x"
            bypass_battery(grid, house, house.route.list_x[-1] + horizontal, house.route.list_y[-1], horizontal, axis)
        
        else:
            house.route.list_x.append(house.route.list_x[-1] + horizontal)
            house.route.list_y.append(house.route.list_y[-1])

    while house.route.list_y[-1] != house.route.battery.position_y:
        
        if house.check == True:
            axis = "y"
            bypass_battery(grid, house, house.route.list_y[-1] + vertical, house.route.list_x[-1], vertical, axis)
        
        else:
            house.route.list_y.append(house.route.list_y[-1] + vertical)
            house.route.list_x.append(house.route.list_x[-1])

    return

def bypass_battery(grid, house, x, y, direction, axis):
    """
    bypasses battery if house is relocated and needed
    Input: grid class, house class, x integer, y integer, direction integer, axis string
    returns: none
    """
    # save non-chosen batteries in list
    other_batteries = []
    for battery in grid.batteries:
        if battery != house.route.battery:
            other_batteries.append(battery)
    
    # check if new coordinated don't lead to other batteries
    for battery in other_batteries:
        
        # bypass other batteries 
        if x == battery.position_x and y == battery.position_y:
            if axis == "x":
                if y == 50:
                    # y-as down
                    house.route.list_y.append(house.route.list_y[-1] - 1, house.route.list_y[-1], house.route.list_y[-1] + 1)
                    # x-as
                    house.route.list_x.append(house.route.list_x[-1], house.route.list_x[-1] + direction, house.route.list_x[-1])

                else:
                    # y-as
                    house.route.list_y.append(house.route.list_y[-1] + 1, house.route.list_y[-1], house.route.list_y[-1] - 1)
                    # x-as
                    house.route.list_x.append(house.route.list_x[-1], house.route.list_x[-1] + direction, house.route.list_x[-1])

            else:
                if x == 50:
                    # x-as down
                    house.route.list_x.append(house.route.list_x[-1] - 1, house.route.list_x[-1], house.route.list_x[-1] + 1)
                    # y-as
                    house.route.list_y.append(house.route.list_y[-1], house.route.list_y[-1] + direction, house.route.list_y[-1])

                    
                else:
                    # x-as
                    house.route.list_x.append(house.route.list_x[-1] + 1, house.route.list_x[-1], house.route.list_x[-1] - 1)
                    # y-as
                    house.route.list_y.append(house.route.list_y[-1], house.route.list_y[-1] + direction, house.route.list_y[-1])
        
        # append if bypasses is not needed
        else:
            # changes x coordinate
            if axis == "x":
                house.route.list_x.append(house.route.list_x[-1] + direction)
                house.route.list_y.append(house.route.list_y[-1])
            # changes y coordinate
            else:
                house.route.list_y.append(house.route.list_y[-1] + direction)
                house.route.list_x.append(house.route.list_x[-1])

    return