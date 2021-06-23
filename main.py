"""
Created by CodeName

This file contains the main function. It asks the user for input on iterations, runs and algorithm. 
Then it runs the algorithm and gets the best state. 
After this, it prints the costs, and visualizes the state and process of the algorithm.
"""

# Import packages
import json
import copy
import time

from sys import argv
from os import path

# Importfiles
from code.algorithms import randomize, greedy, hillclimber, simulatedannealing
from code.classes import grid
from code.visualisation import visualise as vs
from code.output import output


ALGORITHMS = ["RA", "GR", "HC", "SA"]
SIZE_GRID = 50


if __name__ == "__main__":
    
    # Check if command-line contains two arguments
    if len(argv) != 2:
        print("Usage: python3 main.py [district_number]")
        exit(1)


    #------------------------------------------ SETUP GRID ------------------------------------------#
    
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


    # -------------------------------------------- INPUT -------------------------------------------#

    information = f"Choose an algorithm: \n- for Random, type RA \n- for Greedy, type GR \n- for Hillclimber, type HC \n- for Simulated Annealing, type SA \n"
    
    while True:
        algorithm = input(f"{information} : ")

        if algorithm in ALGORITHMS:
            break
    

    #--------------------------------------------- RANDOM ------------------------------------------#

    if algorithm == "RA":
        if argv[1] != "test":
            print("Doesn't work, too slow for 150 houses. Choose test district")
            exit(3)
            
        state = randomize.Randomize(grid)
        copy_grid = state.run()
    
    
    #--------------------------------------------- GREEDY ------------------------------------------#

    if algorithm == "GR":
        
        state = greedy.Greedy(grid)    
        copy_grid = state.run()
    

    #----------------------------- HILL CLIMBER / SIMULATED ANNEALING ------------------------------#

    if algorithm == "HC" or algorithm == "SA":

        iterations = int(input("Choose a number of iterations: "))
        long_run = int(input("Choose a number of runs: "))

        lowest_costs = 99999999999999999999999
        quickest_run = 99999999999999999999999
        total_time = 0

        if algorithm == "HC":
            algorithm_houses = "HC"
            algorithm_cables = "HC"
            temperature = 1
            cooling_scheme = "none"
        else:
            algorithm_houses = input("Choose an algorithm for pairing houses and batteries (HC/SA): ")
            algorithm_cables = input("Choose an algorithm for creating routes (HC/SA): ")
            temperature = int(input("Choose a start temperature: "))
            cooling_scheme = input(f"Choose a cooling scheme \n- for exponential, type exp \n- for linear, type lin\n : ")

        for i in range(long_run):
            print(f"longrun: {i}")
        
            # Copy grid
            copy_grid = copy.deepcopy(grid)

            # Call hillclimber algorithm
            state = hillclimber.Hill_Climber(copy_grid, iterations, temperature, cooling_scheme, algorithm_houses, algorithm_cables) 
            
            # Start time
            start = time.time()

            copy_grid = state.run()
            
            # End time 
            end = time.time()

            # Measure running time, add time of 1 run to total run time
            total_time = total_time + (end - start)

            # Calculate costs
            total_costs = copy_grid.get_costs()
            shared_costs = copy_grid.shared_costs() 

            iterations = output.write_to_file(shared_costs, state)

            if shared_costs < lowest_costs:
                lowest_costs = shared_costs
            if iterations < quickest_run:
                quickest_run = iterations

        # Writes down the best solution in a json-file
        output.create_final(argv[1], lowest_costs, quickest_run, total_time)
        
    else:
        total_costs = copy_grid.get_costs()

    #------------------------------------------ OUTPUT -----------------------------------------------#
    
    # Writes down the solutions in a json-file
    output.create_output(argv[1], total_costs, copy_grid)

    #-------------------------------------------- GET COSTS -------------------------------------------#

    total_costs = copy_grid.get_costs()
    shared_costs = copy_grid.shared_costs() 

    print(f"Total costs of unique cables: {total_costs}")
    print(f"Total costs of shared cables: {shared_costs}")

    #-------------------------------------- VISUALISATION ---------------------------------------------#
    
    # Plot grid with created cables
    vs.visualise_grid(copy_grid, argv[1])

    if algorithm == "SA" or algorithm == "HC":

        # Plot annealing progress
        vs.visualise_annealing(state, algorithm)
