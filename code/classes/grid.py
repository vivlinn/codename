import csv

from .battery import Battery
from .house import House
from .route import Route



class Grid():
    def __init__(self, file_batteries, file_houses):
        self.grid_width = 5
        self.grid_height = 5
        self.batteries = self.load_battery(file_batteries)
        self.houses = self.load_houses(file_houses)
        # self.cable = cable
        
    
    def load_battery(self, file_batteries):
        """
        Load all the batteries into the graph.
        """
        batteries = []
        with open(file_batteries, 'r') as in_file:
            reader = csv.DictReader(in_file)

            id = 0
            for row in reader:
                positie = row['positie']
                position_x_y = positie.split(",")
                position_x = int(position_x_y[0])
                position_y = int(position_x_y[1])
                batteries.append(Battery(id, position_x, position_y, float(row['capaciteit'])))
                id += 1

        return batteries

    def load_houses(self, file_houses):
        """
        Load all the houses into the graph.
        """
        houses = []
        with open(file_houses, 'r') as in_file:
            reader = csv.DictReader(in_file)

            id = 0
            for row in reader:
                houses.append(House(id, float(row['maxoutput']), int(row['x']), int(row['y'])))
                
                id += 1

            
        # houses[0].route = Route(0, [34, 33, 32, 32, 32, 31, 31, 30, 29], [47, 47, 47, 46, 45, 45, 44, 44, 44])
        return houses



    def get_height(self):
        return self.grid_height

    def get_width(self):
        return self.grid_width
