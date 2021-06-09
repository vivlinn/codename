from sys import argv
from code.classes import grid
from code.visualisation import visualise
from code.visualisation import costs
from os import path
from code.algorithms import random_cables
import csv
import pandas as pd


ITERATIONS = 4

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

    total_costs = 0
    counter = 0

    with open('doc/solutions.csv', 'w') as file:
        file.write("Cables\t\tBatteries\t\tTotal\t\t\n")
        for _ in range(ITERATIONS):
            
            print(counter)
            counter += 1
            
            random_cables.random_cables(grid1)
            individual_costs = costs.get_costs(grid1)
            for key in individual_costs.keys():
                file.write("%i\t\t"%(individual_costs[key]))
            file.write("\n")
            
            total_costs += individual_costs['total']

        average_costs = total_costs / ITERATIONS
        file.write("Average costs: %i"%(average_costs))


    # costs = costs.get_costs(grid1)
    # print(costs)

    visualise.visualise(grid1, argv[1])