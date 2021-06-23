"""
Created by CodeName.

This file contains a House class.
Has a max output, x and y coordinates, and route of cables.
"""

from code.classes.route import Route


class House():
    def __init__(self, max_output, position_x, position_y):
        self.max_output = max_output
        self.position_x = position_x
        self.position_y = position_y
        self.route = None
        self.check = False

    def get_x(self):
        """
        Gets the x position of the house

        Returns: int
        """

        return self.position_x

    def get_y(self):
        """
        Gets the y position of the house

        Returns: int
        """

        return self.position_y

    def get_output(self):
        """
        Gets the max output of the house

        Returns: int 
        """   

        return self.max_output

    def get_route(self):
        """
        gets the route class for the house

        Returns: Route class
        """

        return self.route
    
    def set_route(self, battery, x, y):
        """
        Adds a route class to the house

        Returns: none
        """

        self.route = Route(battery, x, y)

    def set_check(self):
        """
        Changes if house needs to be checked

        Returns: none
        """

        if self.check == False:
            self.check = True

        else:
            self.check = False

        return