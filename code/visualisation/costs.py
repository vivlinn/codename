def get_costs(grid):
    """
    This function takes a grid and calculates costs of cables and batteries and the total costs.
    """
    total_length = 0

    for house in grid.houses:
        length = len(house.route.list_x)
        total_length = total_length + length

    cost_cables = total_length * 9
    cost_batteries = len(grid.batteries) * 5000
    total = cost_cables + cost_batteries

    return total

def shared_costs(grid):
    total_x = 0
    total_y = 0
    
    for i in grid.matrix_x:
        for j in i:
            total_x += j
    
    for i in grid.matrix_y:
        for j in i:
            total_y += j

    print(grid.matrix_x)
    print(grid.matrix_y)

    cost_cables = (total_x + total_y) * 9
    cost_batteries = len(grid.batteries) * 5000
    total = cost_cables + cost_batteries
    return int(total)


