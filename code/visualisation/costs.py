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
    
    matrixes = []

    for i in grid.matrix_x:
        for j in i:
            total_x += j
    
    for i in grid.matrix_y:
        for j in i:
            total_y += j

    
    test = [9,8,7,6,5,4,3,2,1,0]
    
    for j in test:
        print(grid.matrix_x[j])
    print()
    # for i in grid.matrix_y:
    for j in test:
        print(grid.matrix_y[j])

    # for i in range(10):
    #     print(i)
    #     print(grid.matrix_x[i])
    # print()
    # for i in range(10, 0):
    #     print(grid.matrix_y[i])

    # print(grid.matrix_x)
    # print(grid.matrix_y)

    cost_cables = (total_x + total_y) * 9
    cost_batteries = len(grid.batteries) * 5000
    total = cost_cables + cost_batteries
    return int(total)


