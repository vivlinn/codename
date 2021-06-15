import json

from sys import argv
from os import path

from code.algorithms import randomize, greedy, simulated_annealing
from code.classes import grid
from code.visualisation import costs, visualise

ITERATIONS = 500000000
TEMPERATURE = 3000

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


    """------------------------------ SIMULATED ANNEALING ----------------------------"""
    state = simulated_annealing.Simulated_annealing(grid, ITERATIONS, TEMPERATURE)

    grid = state.run()

    visualise.visualise_annealing(state)


    """--------------------------------- GET COSTS -----------------------------------"""
    total_costs = costs.get_costs(grid)


    """-----------------------------------OUTPUT--------------------------------------"""
    # Create output
    output = []

    # append district name and total costs
    output.append({"district": argv[1], "costs-shared": total_costs})
    counter = 1

    # append attributes for batteries
    for battery in grid.batteries:
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
    visualise.visualise_grid(grid, argv[1])