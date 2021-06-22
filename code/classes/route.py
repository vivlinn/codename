"""
Created by CodeName.

This file contains a Route class.
Each Route has a specified battery class and a list for the x and y coordinates.
"""


class Route():
    def __init__(self, battery, x, y):
        self.battery = battery
        self.list_x = [x,]
        self.list_y = [y,]