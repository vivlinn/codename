"""
Created by CodeName.

This file contains a random algorithm.


"""

import random
from code.classes.route import Route

class Randomize():
    """
    Random algorithm

    Returns: Grid class
    """

    def __init__(self, grid):
        self.grid = grid

    def run(self):
        """
        Assigns houses to batteries randomly, then randomly lays a route between them

        Returns: Grid class
        """
        
        self.assign_battery()
        self.create_paths()

        return self.grid

    def assign_battery(self):
        """
        Assigns houses to batteries randomly. If succesful for all then creates a route class for each house. 
        If not succesful; exits function

        Returns: Bool
        """

        # Loop through all houses in grid
        for house in self.grid.houses:

            # Loop till a battery is assigned to a house
            while True:

                succes = False
                for battery in self.grid.batteries:
                    if house.max_output <= battery.remaining:
                        succes = True
                        break
                
                # Assign random battery to the house
                battery_chosen = random.choice(self.grid.batteries)

                # Check if battery has capacity for the house
                if battery_chosen.remaining >= house.max_output:

                    # Update remaining battery_chosen capacity
                    battery_chosen.remaining = battery_chosen.remaining - house.max_output
                    break
                
                if succes == False:
                    return succes, self.grid

            # Add route object to the house
            battery_chosen.connected_houses.append(house)
            house.route = Route(battery_chosen, house.position_x, house.position_y)


        return succes, self.grid
        
            
    def create_paths(self):
        """
        Creates random paths from house to battery. 
        Only checks to stay inside grid and not connect to multiple batteries

        Returns: None
        """

        for house in self.grid.houses:

            # Save non-chosen batteries in list
            other_batteries = []
            for battery in self.grid.batteries:
                if battery != house.route.battery:
                    other_batteries.append(battery)


            while house.route.battery.position_x != house.route.list_x[-1] or house.route.battery.position_y != house.route.list_y[-1]:

                direction = random.choice(['x', 'y'])

                if direction == 'x':
                    direction_x = random.choice([-1, 1])
                    x = house.route.list_x[-1] + direction_x
                    y = house.route.list_y[-1]
                    
                    # Check if x-coordinate is within grid
                    if x >= 0 and x <= self.grid.get_width():
                        
                        # Check if route has started
                        if len(house.route.list_x) > 1:
                            # Set previous coordinate as previous
                            previous = house.route.list_x[-2]
                        
                            # Check if new coordinate was not the previous coordinate
                            if previous == x:
                                # Choose new coordinate
                                continue

                        valid = True
                        # Check if new coordinated don't lead to other batteries
                        for battery in other_batteries:
                            
                            # Bypass other batteries 
                            if x == battery.position_x and y == battery.position_y:
                                valid = False
                        
                        if valid == True:
                            # Append new coordinate to route list
                            house.route.list_x.append(x)

                            # Append unchanged y coordinate to route list
                            house.route.list_y.append(y)


                else:
                    direction_y = random.choice([-1, 1])
                    y = house.route.list_y[-1] + direction_y
                    x = house.route.list_x[-1]

                    if y>= 0 and y <= self.grid.get_height():

                        # Check if route has started
                        if len(house.route.list_y) > 1:
                            # Set previous cordinate as previous
                            previous = house.route.list_y[-2]

                            # Check if new coordinate was not the previous coordinate
                            if previous == y:
                                # Choose new coordinate
                                continue

                        valid = True
                        # Check if new coordinated don't lead to other batteries
                        for battery in other_batteries:
                            
                            # Bypass other batteries 
                            if x == battery.position_x and y == battery.position_y:
                                valid = False
                        
                        if valid == True:
                            # append new coordinate to route list
                            house.route.list_x.append(x)

                            # Append unchanged y coordinate to route list
                            house.route.list_y.append(y)
        return