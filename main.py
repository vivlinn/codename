import json
import copy
import time

from sys import argv
from os import path

from code.algorithms import randomize, greedy, hillclimber, simulatedannealing
from code.classes import grid
from code.visualisation import visualise, longrun


SIZE_GRID = 10
ITERATIONS = 5000
TEMPERATURE = 5
LONGRUN = 1
SAME_RESULT_HOUSES = 1000
SAME_RESULT_CABLES = 1000
ALGORITHM_HOUSES = "SA"
ALGORITHM_CABLES = "SA"
COOLING_SCHEME = "exp"

if __name__ == "__main__":
    
    # Check if command-line contains two arguments
    if len(argv) != 2:
        print("Usage: python3 main.py [district_number]")
        exit(1)


    """---------------------------------- SETUP GRID ----------------------------------"""
    
    # Check if folder for district exists
    if not path.exists(f"data/district_{argv[1]}"):
        print("path: for [district_number] does not exist")
        exit(2)

    # Use the correct files for the chosen district
    number = argv[1]

    file_batteries = f"data/district_{number}/district-{number}_batteries.csv"
    file_houses = f"data/district_{number}/district-{number}_houses.csv"
    
    # Create grid with houses and batteries
    grid = grid.Grid(SIZE_GRID, file_batteries, file_houses)

    """ ------------------------------------ INPUT -----------------------------------"""
    information = f"Choose an algorithm: \n for Random, type RA \n for Greedy, type GR \n for Hillclimber, type HC \n for Simulated Annealing, type SA \n "
    algorithm = input(f"{information} :")
    
    """------------------------------------- RANDOM ----------------------------------"""
    if algorithm == "RA":
        if argv[1] != "test":
            print("Doesn't work, too slow for 150 houses. Choose test district")
            exit(3)
            
        state = randomize.Randomize(grid)
        grid = state.run()
    
    
    """------------------------------------- GREEDY ----------------------------------"""
    if algorithm == "GR":
        
        state = greedy.Greedy(grid)    
        copy_grid = state.run()
    

    """------------------------------------- LOOP ------------------------------------"""
    lowest_costs = 99999999999999999999999
    quickest_run = 99999999999999999999999
    total_time = 0

    if algorithm == "HC" or algorithm == "SA":
        algorithm_houses = "HC"
    """------------------------------- HILL CLIMBER-------------------------------"""

    """------------------------------ SIMULATED ANNEALING ------------------------"""
        
        for i in range(LONGRUN):
            print(f"longrun: {i}")
            
        
            # Copy grid
            copy_grid = copy.deepcopy(grid)
            state = hillclimber.Hill_Climber(copy_grid, ITERATIONS, TEMPERATURE, COOLING_SCHEME, ALGORITHM_HOUSES, ALGORITHM_CABLES) 
            
            # Start time
            start = time.time()

            copy_grid = state.run()
            
            # End time 
            end = time.time()

            visualise.visualise_annealing(state)

            # Measure running time, add time of 1 run to total run time
            total_time = total_time + (end - start)

            """--------------------------------- GET COSTS --------------------------------"""
            total_costs = copy_grid.get_costs()
            shared_costs = copy_grid.shared_costs() 

            print(f"without shared cables costs: {total_costs}")
            print(f"shared cables costs (mutate cables): {shared_costs}")

            iterations = longrun.write_to_file(shared_costs, state)

            if shared_costs < lowest_costs:
                lowest_costs = shared_costs
            if iterations < quickest_run:
                quickest_run = iterations

        # Create output
        final = []

        # Append district name and total costs
        final.append({"district": argv[1], "lowest cost": lowest_costs, "quickest run": quickest_run, "total run time": total_time })

        # Save file as json
        final_file = open("output/final_hill.json", "w")
        json.dump(final, final_file, indent = 6)    

        # Close file
        final_file.close()
    else:
        total_costs = copy_grid.get_costs()
        
    """-----------------------------------OUTPUT----------------------------------------"""
    # Create output
    output = []

    # Append district name and total costs
    output.append({"district": argv[1], "costs-shared": total_costs})
    counter = 1

    # Append attributes for batteries
    for battery in copy_grid.batteries:
        output.append({"location": f"{battery.position_x}, {battery.position_y}", "capacity": battery.capacity, "houses": []})
        
        # Append attributes for houses
        for house in battery.connected_houses:
            cables = []

            # Append coordinates of route
            for xi, yi in zip(house.route.list_x, house.route.list_y):
                cables.append(f"{xi}, {yi}")
            
            output[counter]["houses"].append({"location": f"{house.position_x}, {house.position_y}", "output": house.max_output, "cables": cables})

    # Save file as json
    out_file = open("output/output.json", "w")
    json.dump(output, out_file, indent = 6)    

    # Close file
    out_file.close()


    """--------------------------- GRID VISUALISATION ----------------------------------"""
    visualise.visualise_grid(copy_grid, argv[1])