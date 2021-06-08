def get_costs(grid):
    costs = {}
    total_length = 0
    batteries = []

    for house in grid.houses:
        length = len(house.route.list_x)
        total_length = total_length + length

        if not house.route.battery in batteries:
            batteries.append(house.route.battery)

    costs["cables"] = total_length * 9
    costs["batteries"] = len(batteries) * 5000
    costs["total"] = costs["cables"] + costs["batteries"]

    return costs

