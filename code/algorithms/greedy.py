"""
Created by CodeName.

This file contains a greedy algorithm.

"""

from code.classes.route import Route


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
        Then adds all route coordinates to a route class for every house

        Returns: Grid class
        """

        self.create_connections()

        self.create_cables(self.grid.houses)

        return self.grid

    def create_connections(self):
        """
        Adds all houses to closest battery.
        Then removes excessive houses from batteries if needed.
        Then adds houses to other battery with capacity left

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
        checks direction towards the coupled battery and lays cables between.

        List_houses: list

        Returns: Grid class 
        """

        for house in list_houses:
            horizontal, vertical = self.define_direction(house)

            self.lay_cables(house, horizontal, vertical)

        return self.grid

    def rearrange_houses(self, houses_left, sorted_batteries):
        """
        takes all the houses without battery and tries to append them to a battery if possible
        
        houses_left: list
        sorted_batteries: list

        Returns: None
        """

        # Go until no more houses left
        while len(houses_left) > 0:

            # Go till battery isn't too full
            for house in houses_left:
            
                # Iterate over batteries
                for battery in sorted_batteries:

                    # If battery has enough capacity for this house
                    if house.max_output <= battery.remaining:
                        
                        # Connect house to battery
                        house.route = Route(battery, house.position_x, house.position_y)
                        battery.add_house(house)
                        
                        # Update remaining capacity
                        battery.update_remaining(house, "subtract")
                    
                        # Remove house from list
                        houses_left.remove(house)
                        break   

    def remove_excessive_houses(self):
        """
        unconnects houses from battery and appends these left over houses to a list

        Returns: list
        """

        houses_left = []

        # Iterate over batteries
        for battery in self.grid.batteries:
                
            # If battery is full
            while battery.remaining < 0:

                # Remove last house
                house = battery.remove_house()

                # Update houses left
                houses_left.append(house)

                house.check = True

                # Update remainig capacity of battery
                battery.update_remaining(house, "add")
                
            return houses_left

    def define_direction(self, house):
        """
        Get direction for path for x-axis and y-axis by checking the differnce between house and battery coordinates
        
        house: House class

        Returns: horizontal: int, vertical: int
        """

        # If house is further on x-axis than battery: decrease x-coordinate
        if house.route.get_last("x") >= house.route.battery.get_x():
            horizontal = - 1

        # Else increase x-coordinate
        else:
            horizontal = 1

        # If house is further on y-axis than battery: decrease y-coordinate
        if house.route.get_last("y") > house.route.battery.get_y():
            vertical = -1

        # Else increase y-coordinate
        else:
            vertical = 1

        return horizontal, vertical

    def assign_battery(self, house):
        """
        assigns a battery to a house with the least distance between them

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
        house.route = Route(battery_chosen, house.position_x, house.position_y)

        battery_chosen.add_house(house)

        # Update remaining capacity for battery
        battery_chosen.update_remaining(house, "subtract")

        return

    # https://www.programiz.com/python-programming/methods/list/sort
    def bubbleSort(self, arr, object):
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
                    if arr[j].max_output < arr[j + 1].max_output:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                else:
                    if arr[j].remaining > arr[j + 1].remaining:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]

        return arr
        

    def lay_cables(self, house, horizontal, vertical):
        """
        Lays cables from house to battery and adds the coordinates to route class.
        Starts by going horizontal, then vertical until battery is reached.
        house: House class; 
        horizontal: int; 
        vertical: int

        Returns: None
        """
        
        # Save non-chosen batteries in list
        other_batteries = []

        for battery in self.grid.batteries:

            if battery != house.route.battery:
                other_batteries.append(battery)
    
        # Loop till x-coordinate of cable matches x-coordinate of battery
        while house.route.get_last("x") != house.route.battery.get_x():

            # When house is not coupled to closest battery
            if house.check:
                axis = "x"

                # Check if path doesn't cross other batteries
                self.bypass_battery(house, horizontal, vertical, axis, other_batteries)

                # Re-calculate direction from path to battery
                horizontal, vertical = self.define_direction(house)
            else:
                x = house.route.get_last("x") + horizontal
                y = house.route.get_last("y")
                
                house.route.add_cable(x, y)

                # Add cables to matrix
                self.grid.track_shared(x, y, "x", horizontal)

        # Loop till y-coordinate of cable matches y-coordinate of battery
        while house.route.get_last("y") != house.route.battery.get_y():
            # When house is not coupled to closest battery
            if house.check == True:
                axis = "y"

                # Check if path doesn't cross other batteries
                self.bypass_battery(house, horizontal, vertical, axis, other_batteries)

                # Re-calculate direction from path to battery
                horizontal, vertical = self.define_direction(house)
            else:
                y = house.route.get_last("y") + vertical
                x = house.route.get_last("x")

                house.route.add_cable(x, y)
                
                # Add cables to matrix
                self.grid.track_shared(x, y, "y", vertical)

        # Set checking back to
        house.check = False

        return

    def bypass_battery(self, house, horizontal, vertical, axis, other_batteries):
        """
        bypasses battery if house is relocated and needed

        house: House class; 
        horizontal: int; 
        vertical: int;
        axis: string
        other_batteries: list

        returns: None
        """

        x = house.route.get_last("x")
        y = house.route.get_last("y")
  
        # Check if new coordinated don't lead to other batteries
        for battery in other_batteries:
              
            # If path is moving across the x-axis
            if axis == "x":
                
                # Bypass other batteries 
                if x + horizontal == battery.get_x() and y == battery.get_y():

                    # Move one y-coordinate up or down, then one x coordinate left or right depending on direction towards right battery
                    x_move = [x, x + horizontal]
                    y_move = [y + vertical, y + vertical]

                    house.route.add_cable(x_move, y_move)

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

                    house.route.add_cable(x_move, y_move)
                    
                    # Add cables to matrix
                    self.grid.track_shared((x + horizontal), y, "x", horizontal)
                    self.grid.track_shared((x + horizontal), (y + vertical), "y", vertical)

                    return

        # Append if bypasses is not needed
        if axis == "x":
            
            # Changes x-coordinate
            house.route.add_cable(x + horizontal, y)
    
            # Add cables to matrix
            self.grid.track_shared((x + horizontal), y, "x", horizontal)
        else:

            # Changes y-coordinate
            house.route.add_cable(x, y + vertical)
            
            # Add cables to matrix
            self.grid.track_shared(x, (y + vertical), "y", vertical)

        return
