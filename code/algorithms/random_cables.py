import random
from code.classes.route import Route
import queue
import copy

def random_cables(grid):

    for house in grid.houses:

        while True:
            battery = random.choice(grid.batteries)
            if battery.remaining >= house.max_output:
                battery.remaining = battery.remaining - house.max_output
                break

        house.route = Route(battery, house.position_x, house.position_y)

        while not battery.position_x == house.route.list_x[-1] and not battery.position_y == house.route.list_y[-1]:
            

            direction = random.choice(['x', 'y'])

            if direction == 'x':
                direction_x = random.choice([-1, 1])
                xtest = house.route.list_x[-1] + direction_x
                
                if xtest >= 0 and xtest <= grid.grid_width:
                    
                    # print(house.route.list_x[-1])
                    house.route.list_x.append(xtest)
                    ytest = house.route.list_y[-1]
                    house.route.list_y.append(ytest)

            else:
                direction_y = random.choice([-1, 1])
                ytest = house.route.list_y[-1] + direction_y

                if ytest>= 0 and ytest <= grid.grid_height:
                    house.route.list_y.append(ytest)
                    xtest = house.route.list_x[-1]
                    house.route.list_x.append(xtest)

        house.route.list_x.append(battery.position_x)
        house.route.list_y.append(battery.position_y)          

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