def get_costs(grid):
    costs = {}
    total_length = 0

    for house in grid.houses:
        length = len(house.route.list_x)
        total_length = total_length + length


    total_costs = cost_cables + cost_batteries

    costs["cables"] = total_length * 9
    costs["batteries"] = 
    costs["total"] = costs["cables"] + costs["batteries"]
    
    return costs

