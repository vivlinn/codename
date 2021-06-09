from sys import argv
from code.classes import grid
from code.visualisation import visualise
from code.visualisation import costs
from os import path
from code.algorithms import random_cables
import csv
import pandas as pd


if __name__ == "__main__":
    
    # check if command-line contains two arguments
    if len(argv) != 2:
        print("Usage: python3 main.py [district_number]")
        exit(1)
    
    # check if map exists
    if not path.exists(f"data/district_{argv[1]}"):
        print("Usage: python3 main.py [district_number]")
        exit(1)

    number = argv[1]
    
    file_batteries = f"data/district_{number}/district-{number}_batteries.csv"
    file_houses = f"data/district_{number}/district-{number}_houses.csv"
    grid1 = grid.Grid(file_batteries, file_houses)

    
    with open('doc/solutions.csv', 'w') as file:
        file.write("Cables\t\tBatteries\t\tTotal\t\t\n")
        for _ in range(5):
            random_cables.random_cables(grid1)
            total_costs = costs.get_costs(grid1)
            for key in total_costs.keys():
                file.write("%i\t\t"%(total_costs[key]))
            file.write("\n")

    # costs = costs.get_costs(grid1)
    # print(costs)

    visualise.visualise(grid1, argv[1])