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
    
    for matrix in grid.matrix:
        for i in matrix:
            for j in i:
                print(j)
                print(type(j))
                print(type(total_x))

                total_x += j

    test = [9,8,7,6,5,4,3,2,1,0]

    for i in grid.matrix:
        for j in i:
            for k in test:
                print(j[k])

    cost_cables = (total_x + total_y) * 9
    cost_batteries = len(grid.batteries) * 5000
    total = cost_cables + cost_batteries
    return int(total)


