"""
Created by CodeName.

This file contains a greedy algorithm.

"""


class Greedy():
    """
    Greedy algorithm.
    """

    def __init__(self, grid):
        self.grid = grid

    def run(self):
        """
        Runs the greedy algorithm;
        This function tries to assign the closest battery for every house.
        It then checks if the battery capacity is not exceeded, else assigns another battery to the house.
        Then adds all route coordinates to a route class for every house.

        Returns: Grid class
        """

        # Assigns houses to closest batteries
        self.create_connections()

        # Adds routes from houses to batteries
        self.create_cables(self.grid.houses)

        return self.grid

    def create_connections(self):
        """
        Adds all houses to closest battery.
        Then removes excessive houses from batteries if needed.
        Then adds houses to other battery with capacity left.

        Returns: None
        """

        # Sort houses on output
        sorted_output = self.bubbleSort(self.grid.houses, "house")

        for house in sorted_output:

            # Assign closest battery to house
            self.assign_battery(house)

        # Place houses in list until battery not exceeds capacity
        houses_left = self.remove_excessive_houses()

        self.bubbleSort(houses_left, "house")

        sorted_batteries = self.bubbleSort(self.grid.batteries, "battery")

        # Append houses to other batteries
        self.rearrange_houses(houses_left, sorted_batteries)

        return

    def create_cables(self, list_houses):
        """
        Loops through houses in list. 
        Checks direction towards the coupled battery and lays cables between.

        List_houses: list

        Returns: Grid class 
        """

        for house in list_houses:
            route = house.get_route()

            horizontal, vertical = self.define_direction(route)

            self.lay_cables(house, horizontal, vertical)

        return self.grid

    def rearrange_houses(self, houses_left, sorted_batteries):
        """
        Takes all the houses without battery and tries to append them to a battery if possible.

        houses_left: list
        sorted_batteries: list

        Returns: None
        """

        # Go until no more houses left
        while len(houses_left) > 0:

            # Go till battery isn't too full
            for house in houses_left:
            
                for battery in sorted_batteries:

                    # If battery has enough capacity for this house
                    if house.get_output() <= battery.get_remaining():
                        
                        # Connect house to battery
                        house.set_route(battery, house.get_x(), house.get_y())
                        battery.add_house(house)
                        
                        # Update remaining capacity
                        battery.update_remaining(house, "subtract")
                    
                        # Remove house from list
                        houses_left.remove(house)

                        return   

    def remove_excessive_houses(self):
        """
        Unconnects houses from battery and appends these left over houses to a list.

        Returns: list
        """

        houses_left = []

        # Iterate over batteries
        for battery in self.grid.batteries:
                
            # If battery is full
            while battery.get_remaining() < 0:

                # Remove last house
                house = battery.remove_house()

                # Update houses left
                houses_left.append(house)

                house.set_check()

                # Update remainig capacity of battery
                battery.update_remaining(house, "add")
                
            return houses_left

    def define_direction(self, route):
        """
        Get direction for path for x-axis and y-axis by checking the differnce between house and battery coordinates.
        
        route: Route class

        Returns: int, int
        """

        # If house is further on x-axis than battery: decrease x-coordinate
        if route.get_last("x") >= route.battery.get_x():
            horizontal = - 1

        # Else increase x-coordinate
        else:
            horizontal = 1

        # If house is further on y-axis than battery: decrease y-coordinate
        if route.get_last("y") > route.battery.get_y():
            vertical = -1

        # Else increase y-coordinate
        else:
            vertical = 1

        return horizontal, vertical

    def assign_battery(self, house):
        """
        Assigns a battery to a house with the least distance between them.

        house: House class

        Returns: None
        """

        battery_chosen = None

        # Save shortest distance in best, start with longest possible
        best = self.grid.get_height() + self.grid.get_width() + 2

        for battery in self.grid.batteries:

            # Calculate distance between x-coordinates + distance between y-coordinates from house to battery
            distance = abs(battery.get_x() - house.get_x()) + abs(battery.get_y() - house.get_y())

            # If this is shorter than for last battery:
            if distance < best:

                # Update best to shorter distance
                best = distance

                battery_chosen = battery
        
        # Create Route class for house/battery couple
        house.set_route(battery_chosen, house.get_x(), house.get_y())

        battery_chosen.add_house(house)

        # Update remaining capacity for battery
        battery_chosen.update_remaining(house, "subtract")

        return

    def bubbleSort(self, array, object):
        """
        From: https://www.programiz.com/python-programming/methods/list/sort

        Sorts a list using bubble sort.

        Array: list
        Object: str

        Returns: list
        """

        n = len(array)

        # Traverse through all array elements
        for i in range(n-1):

            # Last i elements are already in place
            for j in range(0, n-i-1):

                # Swap if the element found is greater
                if object == "house":
                    if array[j].get_output() < array[j + 1].get_output():
                        array[j], array[j + 1] = array[j + 1], array[j]
                else:
                    if array[j].get_remaining() > array[j + 1].get_remaining():
                        array[j], array[j + 1] = array[j + 1], array[j]

        return array

    def lay_cables(self, house, horizontal, vertical):
        """
        Lays cables from house to battery and adds the coordinates to route class.
        Starts by going horizontal, then vertical until battery is reached.

        house: House class; 
        horizontal: int; 
        vertical: int

        Returns: None
        """
        
        route = house.get_route()

        # Save non-chosen batteries in list
        other_batteries = []

        for battery in self.grid.batteries:

            if battery != route.battery:
                other_batteries.append(battery)
    
        # Loop till x-coordinate of cable matches x-coordinate of battery
        while route.get_last("x") != route.battery.get_x():

            # When house is not coupled to closest battery
            if house.check:
                axis = "x"

                # Check if path doesn't cross other batteries
                self.bypass_battery(route, horizontal, vertical, axis, other_batteries)

                # Re-calculate direction from path to battery
                horizontal, vertical = self.define_direction(route)
            else:
                x = route.get_last("x") + horizontal
                y = route.get_last("y")
                
                route.add_cable(x, y)

                # Add cables to matrix
                self.grid.track_shared(x, y, "x", horizontal)

        # Loop till y-coordinate of cable matches y-coordinate of battery
        while route.get_last("y") != route.battery.get_y():
            # When house is not coupled to closest battery
            if house.check:
                axis = "y"

                # Check if path doesn't cross other batteries
                self.bypass_battery(route, horizontal, vertical, axis, other_batteries)

                # Re-calculate direction from path to battery
                horizontal, vertical = self.define_direction(route)
            else:
                y = route.get_last("y") + vertical
                x = route.get_last("x")

                route.add_cable(x, y)
                
                # Add cables to matrix
                self.grid.track_shared(x, y, "y", vertical)

        # Set checking back to
        house.set_check()

        return

    def bypass_battery(self, route, horizontal, vertical, axis, other_batteries):
        """
        bypasses battery if house is relocated and needed

        route: Route class; 
        horizontal: int; 
        vertical: int;
        axis: string
        other_batteries: list

        returns: None
        """

        x = route.get_last("x")
        y = route.get_last("y")
  
        # Check if new coordinated don't lead to other batteries
        for battery in other_batteries:
              
            # If path is moving across the x-axis
            if axis == "x":
                
                # Bypass other batteries 
                if x + horizontal == battery.get_x() and y == battery.get_y():

                    # Move one y-coordinate up or down, then one x coordinate left or right depending on direction towards right battery
                    x_move = [x, x + horizontal]
                    y_move = [y + vertical, y + vertical]

                    route.add_cable(x_move, y_move)

                    # Add cables to matrix
                    self.grid.track_shared((x + horizontal), (y + vertical), "x", horizontal)
                    self.grid.track_shared(x, (y + vertical), "y", vertical)

                    return

            # Path is moving across the y-axis
            else:

                # Bypass other batteries 
                if x == battery.get_x() and y + vertical == battery.get_y():

                    # Move one x coordinate left or right, then one y-coordinate up or down depending on direction towards right battery
                    x_move = [x + horizontal, x + horizontal]
                    y_move = [y, y + vertical]

                    route.add_cable(x_move, y_move)
                    
                    # Add cables to matrix
                    self.grid.track_shared((x + horizontal), y, "x", horizontal)
                    self.grid.track_shared((x + horizontal), (y + vertical), "y", vertical)

                    return

        # Append if bypasses is not needed
        if axis == "x":
            
            # Changes x-coordinate
            route.add_cable(x + horizontal, y)
    
            # Add cables to matrix
            self.grid.track_shared((x + horizontal), y, "x", horizontal)
        else:

            # Changes y-coordinate
            route.add_cable(x, y + vertical)
            
            # Add cables to matrix
            self.grid.track_shared(x, (y + vertical), "y", vertical)

        return
