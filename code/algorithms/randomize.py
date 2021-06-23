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
        Assigns houses to batteries randomly, then randomly lays a route between them.

        Returns: Grid class.
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

                    if house.get_output() <= battery.get_remaining():
                        succes = True

                        break
                
                # Assign random battery to the house
                battery_chosen = random.choice(self.grid.batteries)

                # Check if battery has capacity for the house
                if battery_chosen.get_remaining() >= house.get_output():

                    # Update remaining battery_chosen capacity
                    battery_chosen.update_remaining(house, "subtract")
                    break
                
                if succes == False:
                    return succes, self.grid

            # Add route object to the house
            battery_chosen.connected_houses.append(house)
            house.route = Route(battery_chosen, house.get_x(), house.get_y())

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


            while house.route.battery.get_x()!= house.route.get_last("x") or house.route.battery.get_y() != house.route.get_last("y"):

                direction = random.choice(['x', 'y'])

                if direction == 'x':
                    direction_x = random.choice([-1, 1])
                    x = house.route.get_last("x") + direction_x
                    y = house.route.get_last("y")
                    
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
                            if x == battery.get_x() and y == battery.get_y():
                                valid = False
                        
                        if valid == True:
                            # Append new coordinates to route list
                            house.route.add_cable(x, y)

                else:
                    direction_y = random.choice([-1, 1])
                    y = house.route.get_last("y") + direction_y
                    x = house.route.get_last("x")

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
                            if x == battery.get_x() and y == battery.get_y():
                                valid = False
                        
                        if valid == True:
                            # Append new coordinates to route list
                            house.route.add_cable(x, y)
        return