import csv
import pandas as pd
import json

from sys import argv
from os import path

from code.algorithms import randomize, greedy, simulated_annealing
from code.classes import grid
from code.visualisation import costs, visualise



if __name__ == "__main__":
    
    # Check if command-line contains two arguments
    if len(argv) != 2:
        print("Usage: python3 main.py [district_number]")
        exit(1)


    # ---------------------------------- SETUP GRID ----------------------------------
    
    # Check if folder for district exists
    if not path.exists(f"data/district_{argv[1]}"):
        print("Usage: python3 main.py [district_number]")
        exit(1)

    # Use the correct files for the chosen district
    number = argv[1]

    file_batteries = f"data/district_{number}/district-{number}_batteries.csv"
    file_houses = f"data/district_{number}/district-{number}_houses.csv"
    
    # Create grid with houses and batteries
    grid = grid.Grid(file_batteries, file_houses)
    
    
    # ------------------------------------- GREEDY ----------------------------------
    # greedy.greedy(grid)    

    # ------------------------------ SIMULATED ANNEALING ----------------------------
    state = simulated_annealing.simulated_annealing(grid)

    grid = state.run()


    # --------------------------------- GET COSTS -----------------------------------
    total_costs = costs.get_costs(grid)

    # -----------------------------------OUTPUT--------------------------------------
    # Create output
    output = []
    output.append({"district": argv[1], "costs-shared": total_costs})
    counter = 1

    # Calculate total costs for grid
    for battery in grid.batteries:
        output.append({"location": f"{battery.position_x}, {battery.position_y}", "capacity": battery.capacity, "houses": []})
        
        for house in battery.connected_houses:
            cables = []
            for xi, yi in zip(house.route.list_x, house.route.list_y):
                cables.append(f"{xi}, {yi}")
            
            output[counter]["houses"].append({"location": f"{house.position_x}, {house.position_y}", "output": house.max_output, "cables": cables})

    out_file = open("output/output.json", "w")
    json.dump(output, out_file, indent = 6)    
    out_file.close()


    

    # --------------------------- MAKE VISUALISATION ----------------------------------
    visualise.visualise(grid, argv[1])