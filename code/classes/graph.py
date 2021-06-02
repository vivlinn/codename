import csv

from . import Battery, House, Cable


class Graph():
    def __init__(self, file_batteries, file_houses):
        self.battery = self.load_battery(file_batteries)
        self.house = self.load_house(file_houses)
        self.cable = cable
        
    
    def load_battery(self, file_batteries):
        """
        Load all the batteries into the graph.
        """
        batteries = {}
        with open(file_batteries, 'r') as in_file:
            reader = csv.DictReader(in_file)

            id = 0
            for row in reader:
                positie = row['positie']
                position_x_y = positie.split(",")
                position_x = position_x_y[0]
                position_y = position_x_y[1]
                batteries[id] = Battery(position_x, position_y, row['capaciteit'])
                id += 1

        return batteries

    def load_houses(self, file_houses):
        """
        Load all the houses into the graph.
        """
        houses = {}
        with open(file_houses, 'r') as in_file:
            reader = csv.DictReader(in_file)

            id = 0
            for row in reader:
                houses[id] = House(row['x'], row['y'], row['maxoutput'])
                id += 1

        return houses