"""
Created by CodeName.

This file contains a Battery class.

Imported in Grid class.

Has coordinates, capacity and a list of House classes.
"""


class Battery():
    def __init__(self, position_x, position_y, capacity):
        self.capacity = capacity
        self.remaining = self.capacity
        self.position_x = position_x
        self.position_y = position_y
        self.connected_houses = []

    def get_x(self):
        """
        Gets the x position of the battery.

        Returns: int
        """

        return self.position_x

    def get_y(self):
        """
        Gets the y position of the battery.

        Returns: int
        """

        return self.position_y  

    def add_house(self, house):
        """
        Connect house to battery.

        house: House class

        Returns: none
        """

        self.connected_houses.append(house)

        return
    
    def remove_house(self):
        """
        Disconnect house from battery.

        Returns: House class
        """

        house = self.connected_houses.pop()

        return house

    def update_remaining(self, house, change):
        """
        Change remaining capacity of battery.

        house: House class
        change: str

        Returns: none
        """

        if change == "add":
            self.capacity += house.max_output
        else:
            self.capacity -= house.max_output

        return


    def get_remaining(self):
        """
        Get remaining capacity of battery.

        Returns: int
        """

        return self.remaining
