CABLE_PRICE = 9
BATTERY_PRICE = 5000

def get_costs(grid):
    """
    This function takes a grid and calculates costs of cables and batteries and the total costs.
    """
    total_length = 0

    for house in grid.houses:
        length = len(house.route.list_x) - 1
        total_length = total_length + length

    cost_cables = total_length * CABLE_PRICE
    cost_batteries = len(grid.batteries) * BATTERY_PRICE
    total = cost_cables + cost_batteries

    return total

def shared_costs(grid):
    """
    This function takes a grid and calculates costs of shared cables and batteries and the total costs.
    """
    total = 0

    for direction in grid.matrix:
        for i in grid.matrix[direction]:            
            for j in i:

                total += j

    cost_cables = (total) * CABLE_PRICE
    cost_batteries = len(grid.batteries) * BATTERY_PRICE
    total = cost_cables + cost_batteries
    return int(total)


