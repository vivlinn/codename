from sys import argv
from code.classes import grid
from code.visualisation import visualise
from os import path
from code.algorithms import random_cables


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

    random_cables.random_cables(grid1)

    visualise.visualise(grid1, argv[1])