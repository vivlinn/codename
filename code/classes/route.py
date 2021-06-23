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

    def add_cable(self, x, y):
        """
        Adds x and y coordinate to list of cable points

        x: int / list
        y: int / list

        Returns: none
        """

        if type(x) == int:
            self.list_x.append(x)
            self.list_y.append(y)
        else:
            self.list_x.extend(x)
            self.list_y.extend(y)

        return
    
    def get_last(self, axis)

        if axis == "x"
            return self.list_x[-1]
        
        return self.list_y[-1]
        

