import random
from code.classes.route import Route
import queue
import copy

def better_cables(grid):

    # loop through all houses in grid
    for house in grid.houses:
        battery_chosen = None
        best = 101
        for battery in grid.batteries:
            distance = abs(battery.position_x, house.position_x) + abs(battery.position_y, house.position_y)
            if distance < best:
                best = distance
                battery_chosen = battery
            

        # add route object to the house
        house.route = Route(battery_chosen, house.position_x, house.position_y)

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


