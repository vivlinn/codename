"""
Created by CodeName.

This file contains functions that write solutions into json-files.
"""

# Importfunctions
import json
from json.decoder import JSONDecodeError

def write_to_file(total_costs, state):
    """
    Saves results from longrunning the algorithms in a file.
    """

    _, y = state.plot()
    
    with open('output/longrun.json', 'a+') as infile:
        try:
            data = json.load(infile)
        except JSONDecodeError:
            data = []
            pass

    # Convert data to list if not
    if type(data) is dict:
        data = [data]

    dictionary = {"costs": total_costs, "iterations": len(y)}

    # Append new item to data lit
    data.append(dictionary)

    # Write list to file
    with open('output/longrun.json', 'w') as outfile:
        json.dump(data, outfile)

    return len(y)

def create_output(district, costs, grid):    
   
    output = []

    # Append district name and total costs
    output.append({"district": district, "costs-shared": costs})
    counter = 1

    # Append attributes for batteries
    for battery in grid.batteries:
        output.append({"location": f"{battery.get_x()}, {battery.get_y()}", "capacity": battery.capacity, "houses": []})
        
        # Append attributes for houses
        for house in battery.connected_houses:
            route = house.get_route()
            cables = []

            # Append coordinates of route
            for xi, yi in zip(route.list_x, route.list_y):
                cables.append(f"{xi}, {yi}")
            
            output[counter]["houses"].append({"location": f"{house.get_x()}, {house.get_y()}", "output": house.get_output(), "cables": cables})

    # Save file as json
    out_file = open("output/output.json", "w")
    json.dump(output, out_file, indent = 6)    

    # Close file
    out_file.close()

def create_final(district, costs, quickest, time):

    final = []

    # Append district name and total costs
    final.append({"district": district, "lowest cost": costs, "quickest run": quickest, "total run time": time})

    # Save file as json
    final_file = open("output/final.json", "w")
    json.dump(final, final_file, indent = 6)    

    # Close file
    final_file.close()
