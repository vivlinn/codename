from code.algorithms.simulated_annealing import simulated_annealing
from sys import argv
from code.classes import grid
from code.visualisation import visualise
from code.visualisation import costs
from os import path
from code.algorithms import random, greedy, simulated_annealing
import csv
import pandas as pd
import json


ITERATIONS = 10

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
    grid = grid.Grid(file_batteries, file_houses)

    # total_costs = 0
    # counter = 0

    # with open('output/solutions.csv', 'w') as file:
    #     file.write("Cables\t\tBatteries\t\tTotal\t\t\n")
    #     for _ in range(ITERATIONS):
            
    #         print(counter)
    #         counter += 1
            
    #         random_cables.random_cables(grid)
    #         individual_costs = costs.get_costs(grid)
    #         for key in individual_costs.keys():
    #             file.write("%i\t\t"%(individual_costs[key]))
    #         file.write("\n")
            
    #         total_costs += individual_costs['total']

    #     average_costs = total_costs / ITERATIONS
    #     file.write("Average costs: %i"%(average_costs))

    # output = []
    # output.append({"district": argv[1], "costs-shared": total_costs})
    # counter = 1
    # for battery in grid.batteries:
    #     output.append({"location": f"{battery.position_x}, {battery.position_y}", "capacity": battery.capacity, "houses": []})
        
    #     for house in battery.connected_houses:
    #         cables = []
    #         for xi, yi in zip(house.route.list_x, house.route.list_y):
    #             cables.append(f"{xi}, {yi}")
            
    #         output[counter]["houses"].append({"location": f"{house.position_x}, {house.position_y}", "output": house.max_output, "cables": cables})

    # out_file = open("output/output.json", "w")
    # json.dump(output, out_file, indent = 6)    
    # out_file.close()

    # print(output[counter])

    # greedy.greedy(grid)

    state = simulated_annealing.simulated_annealing(grid)

    # print()
    # for house in grid.houses:
    #     if house.position_x == 19 and house.position_y == 12:
    #         print(house.route.battery.position_x)
    #     if house.position_x == 30 and house.position_y == 12:
    #         print(house.route.battery.position_x)

    # costs = costs.get_costs(grid1)
    # print(costs)

    visualise.visualise(state, argv[1])