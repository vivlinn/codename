
from code.classes import grid
from code.visualisation import visualise


if __name__ == "__main__":
    file_batteries = f"data/district_1/district-1_batteries.csv"
    file_houses = f"data/district_1/district-1_houses.csv"
    grid1 = grid.Grid(file_batteries, file_houses)

    visualise.visualise(grid1)