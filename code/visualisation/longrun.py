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

