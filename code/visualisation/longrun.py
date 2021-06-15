import json

def write_to_file(total_costs, state):

    _, y = state.plot()
    
    data = json.load(open('output/longrun.json'))

    # convert data to list if not
    if type(data) is dict:
        data = [data]

    dictionary = {"costs": total_costs, "iterations": len(y)}

    # append new item to data lit
    data.append(dictionary)

    # write list to file
    with open('output/longrun.json', 'w') as outfile:
        json.dump(data, outfile)

    return len(y)
