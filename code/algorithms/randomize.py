import random
from code.classes.route import Route

class randomize():
    """
    This function assigns a house randomly to a battery and creates randomly a route between these two.
    
    grid: Grid class

    Returns: None
    """
    def __init__(self, grid):
        self.grid = grid

    def run(self):
        self.assign_battery()
        self.create_paths()


    def assign_battery(self):

        # loop through all houses in grid
        for house in self.grid.houses:

            # loop till a battery is assigned to a house
            while True:

                succes = False
                for battery in self.grid.batteries:
                    if house.max_output <= battery.remaining:
                        succes = True
                        break
                
                # assign random battery to the house
                battery_chosen = random.choice(self.grid.batteries)

                # check if battery has capacity for the house
                if battery_chosen.remaining >= house.max_output:

                    # update remaining battery_chosen capacity
                    battery_chosen.remaining = battery_chosen.remaining - house.max_output
                    break
                
                if succes == False:
                    return succes

            # add route object to the house
            battery_chosen.connected_houses.append(house)
            house.route = Route(battery_chosen, house.position_x, house.position_y)


        return succes
        
            
    def create_paths(self):
        for house in self.grid.houses:

            # save non-chosen batteries in list
            other_batteries = []
            for battery in self.grid.batteries:
                if battery != house.route.battery:
                    other_batteries.append(battery)


            while house.route.battery.position_x != house.route.list_x[-1] or house.route.battery.position_y != house.route.list_y[-1]:

                direction = random.choice(['x', 'y'])

                if direction == 'x':
                    direction_x = random.choice([-1, 1])
                    xtest = house.route.list_x[-1] + direction_x
                    ytest = house.route.list_y[-1]
                    
                    # check if still inside grid
                    if xtest >= 0 and xtest <= self.grid.grid_width:
                        
                        # check if route has started
                        if len(house.route.list_x) > 1:
                            # set previous cordinate as previous
                            previous = house.route.list_x[-2]
                        
                            # check if new coordinate was not the previous coordinate
                            if previous == xtest:
                                # choose new coordinate
                                continue

                        valid = True
                        # check if new coordinated don't lead to other batteries
                        for battery in other_batteries:
                            
                            # bypass other batteries 
                            if xtest == battery.position_x and ytest == battery.position_y:
                                valid = False
                        
                        if valid == True:
                            # append new coordinate to route list
                            house.route.list_x.append(xtest)

                            # append unchanged y coordinate to route list
                            house.route.list_y.append(ytest)


                else:
                    direction_y = random.choice([-1, 1])
                    ytest = house.route.list_y[-1] + direction_y
                    xtest = house.route.list_x[-1]

                    if ytest>= 0 and ytest <= self.grid.grid_height:

                        # check if route has started
                        if len(house.route.list_y) > 1:
                            # set previous cordinate as previous
                            previous = house.route.list_y[-2]

                            # check if new coordinate was not the previous coordinate
                            if previous == ytest:
                                # choose new coordinate
                                continue

                        valid = True
                        # check if new coordinated don't lead to other batteries
                        for battery in other_batteries:
                            
                            # bypass other batteries 
                            if xtest == battery.position_x and ytest == battery.position_y:
                                valid = False
                        
                        if valid == True:
                            # append new coordinate to route list
                            house.route.list_x.append(xtest)

                            # append unchanged y coordinate to route list
                            house.route.list_y.append(ytest)
