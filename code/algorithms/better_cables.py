import random
from code.classes.route import Route
import queue
import copy

def better_cables(grid):

    sorted_output = bubbleSort(grid.houses)

    # loop through all houses in grid
    for house in sorted_output:

        # assign closest battery to house
        assign_battery(grid)

    houses_left = []

    # iterate over batteries
    for battery in grid.batteries:
            
        # if battery is full
        while battery.remaining < 0:
            # remove last house
            house = battery.connected_houses.pop()
            # update houses left
            houses_left.append(house)
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
                    battery.connected_houses.append(house)
                    # update remaining capacity
                    battery.remaining -= house.max_output
                    # remove house from list
                    houses_left.remove(house)
                    break

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

        




        # add route object to the house
        # house.route = Route(battery_chosen, house.position_x, house.position_y)

        # # save non-chosen batteries in list
        # other_batteries = []
        # for battery in grid.batteries:
        #     if battery != battery_chosen:
        #         other_batteries.append(battery) 

        # while battery_chosen.position_x != house.route.list_x[-1] or battery_chosen.position_y != house.route.list_y[-1]:

        #     direction = random.choice(['x', 'y'])

        #     if direction == 'x':
        #         direction_x = random.choice([-1, 1])
        #         xtest = house.route.list_x[-1] + direction_x
        #         ytest = house.route.list_y[-1]
                
        #         # check if still inside grid
        #         if xtest >= 0 and xtest <= grid.grid_width:
                    
        #             # check if route has started
        #             if len(house.route.list_x) > 1:
        #                 # set previous cordinate as previous
        #                 previous = house.route.list_x[-2]
                    
        #                 # check if new coordinate was not the previous coordinate
        #                 if previous == xtest:
        #                     # choose new coordinate
        #                     continue

        #             valid = True
        #             # check if new coordinated don't lead to other batteries
        #             for battery in other_batteries:
                        
        #                 # bypass other batteries 
        #                 if xtest == battery.position_x and ytest == battery.position_y:
        #                     valid = False
                    
        #             if valid == True:
        #                 # append new coordinate to route list
        #                 house.route.list_x.append(xtest)

        #                 # append unchanged y coordinate to route list
        #                 house.route.list_y.append(ytest)


        #     else:
        #         direction_y = random.choice([-1, 1])
        #         ytest = house.route.list_y[-1] + direction_y
        #         xtest = house.route.list_x[-1]

        #         if ytest>= 0 and ytest <= grid.grid_height:

        #             # check if route has started
        #             if len(house.route.list_y) > 1:
        #                 # set previous cordinate as previous
        #                 previous = house.route.list_y[-2]

        #                 # check if new coordinate was not the previous coordinate
        #                 if previous == ytest:
        #                     # choose new coordinate
        #                     continue

        #             valid = True
        #             # check if new coordinated don't lead to other batteries
        #             for battery in other_batteries:
                        
        #                 # bypass other batteries 
        #                 if xtest == battery.position_x and ytest == battery.position_y:
        #                     valid = False
                    
        #             if valid == True:
        #                 # append new coordinate to route list
        #                 house.route.list_x.append(xtest)

        #                 # append unchanged y coordinate to route list
        #                 house.route.list_y.append(ytest)

        # print(house.route.list_x) 
        # print(house.route.list_y)  
        # print()      


