def get_costs(grid):
    """
    This function takes a grid and calculates costs of cables and batteries and the total costs.
    """
    costs = {}
    total_length = 0
    batteries = []

    for house in grid.houses:
        length = len(house.route.list_x)
        total_length = total_length + length

        if not house.route.battery in batteries:
            batteries.append(house.route.battery)

    # Save the costs in a dictionary
    costs["cables"] = total_length * 9
    costs["batteries"] = len(batteries) * 5000
    costs["total"] = costs["cables"] + costs["batteries"]

    return costs["total"]

