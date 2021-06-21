import json

def write_to_file(total_costs, state):
    """
    Saves results from longrunning the algorithms and saves in a file.
    """

    _, y = state.plot()
    
    data = json.load(open('output/longrun_hill.json'))

    # Convert data to list if not
    if type(data) is dict:
        data = [data]

    dictionary = {"costs": total_costs, "iterations": len(y)}

    # Append new item to data lit
    data.append(dictionary)

    # Write list to file
    with open('output/longrun_hill.json', 'w') as outfile:
        json.dump(data, outfile)

    return len(y)

