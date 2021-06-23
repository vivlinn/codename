"""
Created by CodeName.

This file contains a Grid class.
Has a specified size, list of battery classes, list of house classes, and 4 matrices.
"""

# Import packages
import csv
import numpy as np

# Importfiles
from .battery import Battery
from .house import House

# Global variables
CABLE_PRICE = 9
BATTERY_PRICE = 5000


class Grid():
    def __init__(self, size, file_batteries, file_houses):
        self.width = size
        self.height = size
        self.batteries = self.load_battery(file_batteries)
        self.houses = self.load_houses(file_houses)
        self.matrix = self.matrices()

    def matrices(self):
        """
        Create matrices to track shared cables.
        """

        self.matrix = {}
        directions = ["left", "right", "up", "down"]

        for direction in directions:       
            self.matrix[direction] = np.zeros([self.width + 1, self.height + 1], dtype=int)
        
        return self.matrix

    
    def load_battery(self, file_batteries):
        """
        Load all the batteries into the graph.

        file_batteries: path

        Returns: list

        """

        batteries = []
        with open(file_batteries, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for row in reader:
                positie = row['positie']
                position_x_y = positie.split(",")
                position_x = int(position_x_y[0])
                position_y = int(position_x_y[1])
                
                batteries.append(Battery(position_x, position_y, float(row['capaciteit'])))

        return batteries

    def load_houses(self, file_houses):
        """
        Load all the houses into the graph.

        file_houses: path

        Returns: list
        """

        houses = []
        with open(file_houses, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for row in reader:
                houses.append(House(float(row['maxoutput']), int(row['x']), int(row['y'])))
                

        return houses

    def get_height(self):
        """
        Get height of the grid.

        Returns: int
        """

        return self.height

    def get_width(self):
        """
        Get weigth of the grid.

        Returns: int
        """

        return self.width

    def track_shared(self, x, y, axis, direction):
        """
        Keep track of shared cables.

        x: int
        y: int
        axis: str
        direction: str

        Returns: none

        """

        if axis == "x":
            if direction > 0:
                matrix = self.matrix["right"]
            else:
                matrix = self.matrix["left"]
                
        else:
            if direction > 0:
                matrix = self.matrix["up"]
            else:
                matrix = self.matrix["down"]

        matrix[x][y] += 1
    
        return self

    def remove_shared(self, house):
        """
        Remove track of shared cables.

        house: House class

        Returns: class
        """
   
        for i in range(1, len(house.route.list_x)):
    
            if house.route.list_x[-i] == house.route.list_x[-(i+1)]:

                if house.route.list_y[-i] > house.route.list_y[-(i+1)]:
                    matrix = self.matrix["up"]
                else: 
                    matrix = self.matrix["down"]
                  
            else:

                if house.route.list_x[-i] > house.route.list_x[-(i+1)]:
                    matrix = self.matrix["right"]  
                else:
                    matrix = self.matrix["left"]
    
            matrix[house.route.list_x[-(i)]][house.route.list_y[-(i)]] -= 1

        return self

    def get_costs(self):
        """
        This function takes a grid and calculates costs of cables and batteries and the total costs.

        Returns: class
        """

        total_length = 0

        for house in self.houses:
            length = len(house.route.list_x) - 1
            total_length = total_length + length

        cost_cables = total_length * CABLE_PRICE
        cost_batteries = len(self.batteries) * BATTERY_PRICE
        total = cost_cables + cost_batteries

        return total

    def shared_costs(self):
        """
        This function takes a grid and calculates costs of shared cables and batteries and the total costs.

        Returns: int
        """
        total = 0

        for direction in self.matrix:
            for i in self.matrix[direction]:       
                for j in i:

                    if j > 0:
                        total += 1

        cost_cables = (total) * CABLE_PRICE
        cost_batteries = len(self.batteries) * BATTERY_PRICE
        total = cost_cables + cost_batteries

        return int(total)