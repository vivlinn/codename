import json
import copy
import time

from sys import argv
from os import path

from code.algorithms import randomize, greedy, simulated_annealing
from code.classes import grid
from code.visualisation import costs, visualise, longrun

ITERATIONS = 60000
TEMPERATURE = 1000
LONGRUN = 50

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
    grid = grid.Grid(file_batteries, file_houses)
    
    """------------------------------------- RANDOM ----------------------------------"""
    # Doesn't work (too slow for 150 houses)

    # state = randomize.Randomize(grid)
    # grid = state.run()
    
    
    """------------------------------------- GREEDY ----------------------------------"""
    # state = greedy.Greedy(grid)    
    # grid = state.run()

    """------------------------------------- LOOP ----------------------------------"""
    lowest_costs = 99999999999999999999999
    quickest_run = 99999999999999999999999
    total_time = 0

    for i in range(LONGRUN):
        print(f"longrun: {i}")
        
        """------------------------------ SIMULATED ANNEALING ----------------------------"""
        # copy grid
        copy_grid = copy.deepcopy(grid)
        state = simulated_annealing.Simulated_annealing(copy_grid, ITERATIONS, TEMPERATURE)

        # start time
        start = time.time()

        copy_grid, tmp = state.run()
         
        # end time 
        end = time.time()

        visualise.visualise_annealing(state)

        # add time of 1 run to total run time
        total_time = total_time + (end - start)

        """--------------------------------- GET COSTS -----------------------------------"""
        total_costs = costs.shared_costs(tmp)
        shared_costs = costs.shared_costs(copy_grid) 

        print(f"without shared cables costs: {total_costs}")
        print(f"shared cables costs (mutate cables): {shared_costs}")

        iterations = longrun.write_to_file(shared_costs, state)

        if shared_costs < lowest_costs:
            lowest_costs = shared_costs
        if iterations < quickest_run:
            quickest_run = iterations

    # Create output
    final = []

    # append district name and total costs
    final.append({"district": argv[1], "lowest cost": lowest_costs, "quickest run": quickest_run, "total run time": total_time })

    # save file as json
    final_file = open("output/final_hill.json", "w")
    json.dump(final, final_file, indent = 6)    

    # close file
    final_file.close()

    """-----------------------------------OUTPUT--------------------------------------"""
    # Create output
    output = []

    # append district name and total costs
    output.append({"district": argv[1], "costs-shared": total_costs})
    counter = 1

    # append attributes for batteries
    for battery in copy_grid.batteries:
        output.append({"location": f"{battery.position_x}, {battery.position_y}", "capacity": battery.capacity, "houses": []})
        
        # append attributes for houses
        for house in battery.connected_houses:
            cables = []

            # append coordinates of route
            for xi, yi in zip(house.route.list_x, house.route.list_y):
                cables.append(f"{xi}, {yi}")
            
            output[counter]["houses"].append({"location": f"{house.position_x}, {house.position_y}", "output": house.max_output, "cables": cables})

    # save file as json
    out_file = open("output/output.json", "w")
    json.dump(output, out_file, indent = 6)    

    # close file
    out_file.close()


    """--------------------------- GRID VISUALISATION ----------------------------------"""
    visualise.visualise_grid(copy_grid, argv[1])