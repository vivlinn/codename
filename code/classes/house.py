"""
Created by CodeName.

This file contains a House class.
Has a max output, x and y coordinates, and route of cables.
"""


class House():
    def __init__(self, max_output, position_x, position_y):
        self.max_output = max_output
        self.position_x = position_x
        self.position_y = position_y
        self.route = None
        self.check = False


    def get_x(self):

        return self.position_x

    def get_y(self):

        return self.position_y
        