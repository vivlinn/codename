import random
from code.classes.route import Route
import queue
import copy

def random_cables(grid):

    for house in grid.houses:

        while True:
            battery_chosen = random.choice(grid.batteries)
            if battery_chosen.remaining >= house.max_output:

                # update remaining battery_chosen capacity
                battery_chosen.remaining = battery_chosen.remaining - house.max_output
                break

        house.route = Route(battery_chosen, house.position_x, house.position_y)

        while battery_chosen.position_x != house.route.list_x[-1] or battery_chosen.position_y != house.route.list_y[-1]:

            direction = random.choice(['x', 'y'])

            if direction == 'x':
                direction_x = random.choice([-1, 1])
                xtest = house.route.list_x[-1] + direction_x
                ytest = house.route.list_y[-1]
                
                # check if still inside grid
                if xtest >= 0 and xtest <= grid.grid_width:
                    
                    # check if route has started
                    if len(house.route.list_x) > 1:
                        # set previous cordinate as previous
                        previous = house.route.list_x[-2]
                    
                        # check if new coordinate was not the previous coordinate
                        if previous == xtest:
                            # choose new coordinate
                            continue

                    for battery in grid.batteries:
                        
                        # bypass other batteries 
                        if (xtest != battery.position_x or ytest != battery.position_y) and battery is battery_chosen:
                    
                            # append new coordinate to route list
                            house.route.list_x.append(xtest)

                            # append unchanged y coordinate to route list
                            house.route.list_y.append(ytest)
                            break

            else:
                direction_y = random.choice([-1, 1])
                ytest = house.route.list_y[-1] + direction_y
                xtest = house.route.list_x[-1]

                if ytest>= 0 and ytest <= grid.grid_height:

                    # check if route has started
                    if len(house.route.list_y) > 1:
                        # set previous cordinate as previous
                        previous = house.route.list_y[-2]

                        # check if new coordinate was not the previous coordinate
                        if previous == ytest:
                            # choose new coordinate
                            continue

                    for battery in grid.batteries:

                        # bypass other batteries 
                        if ytest != battery.position_y or xtest != battery.position_x or battery is battery_chosen:
                            
                            # append new coordinate to route list
                            house.route.list_y.append(ytest)

                            # append unchanged y coordinate to route list
                            house.route.list_x.append(xtest)
                            break








        print(house.route.list_x) 
        print(house.route.list_y)  
        print()      

        # print()
        # print(house.route.list_x)
        # print(house.route.list_y)
        # print()






#         depth = 20
# depth = 3
# queue = queue.Queue()
# queue.put("")
# while not queue.empty():
#     state = queue.get()
#     print(state)
#     if len(state) < depth:
#         for i in [ '1', '2']:
#             child = copy.deepcopy(state)
#             child += i
#             queue.put(child)