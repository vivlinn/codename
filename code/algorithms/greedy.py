from code.classes.route import Route

class Greedy():
    """
    Greedy algorithm.

    Returns: Grid class
    """

    def __init__(self, grid):
        self.grid = grid

    def run(self):
        """
        Runs the greedy algorithm;
        This function tries to assign the closest battery for every house.
        It then checks if battery capacity is not exceeded, else assigns another battery to the house.
        Then adds all route coordinates to a route class for every house

        Returns: Grid class
        """

        self.create_connections()
        self.create_cables()

        return self.grid

    def create_connections(self):
        """
        Adds all houses to closest battery. 
        Then removes excessive houses from batteries if needed. 
        Then adds houses to other battery with capacity left

        Returns: None
        """
        
        sorted_output = self.bubbleSort(self.grid.houses, "house")

        # loop through all houses in grid
        for house in sorted_output:

            # assign closest battery to house
            self.assign_battery(self.grid, house)

        houses_left = self.remove_excessive_houses()

        self.bubbleSort(houses_left, "house")
        sorted_batteries = self.bubbleSort(self.grid.batteries, "battery")

        self.rearrange_houses(houses_left, sorted_batteries)

        return

    def create_cables(self, list_houses):
        """
        loops through houses in list. 
        checks direction towards the coupled battery and lays cables between.

        list_houses: list

        Returns: Grid class 
        """

        for house in list_houses:
            horizontal, vertical = self.define_direction(house)
            

            self.lay_cables(house, horizontal, vertical)
        
        return self.grid


    def rearrange_houses(houses_left, sorted_batteries):
        """
        takes all the houses without battery and tries to append them to a battery if possible
        
        houses_left: list
        sorted_batteries: list

        Returns: None
        """

        # go until no more houses left
        while len(houses_left) > 0:

        # go till battery isn't too full
            for house in houses_left:
            
                # iterate over batteries
                for battery in sorted_batteries:

                    # if battery has enough capacity for this house
                    if house.max_output <= battery.remaining:
                        
                        # connect house to battery
                        house.route = Route(battery, house.position_x, house.position_y)
                        battery.add_house(house)
                        
                        # update remaining capacity
                        battery.update_remaining(house, "subtract")
                    
                        # remove house from list
                        houses_left.remove(house)
                        break   

    def remove_excessive_houses(self):
        """
        unconnects houses from battery and appends these left over houses to a list

        Returns: list
        """

        houses_left = []

        # iterate over batteries
        for battery in self.grid.batteries:
                
            # if battery is full
            while battery.remaining < 0:

                # remove last house
                house = battery.remove_house()

                # update houses left
                houses_left.append(house)

                house.check = True

                # update remainig capacity of battery
                battery.update_remaining(house, "add")
                
            return houses_left


    def define_direction(self, house):
        """
        Get direction for path for x-axis and y-axis by checking the differnce between house and battery coordinates
        
        house: House class

        Returns: horizontal: int, vertical: int
        """

        # if house is further on x-axis than battery: decrease x-coordinate
        if house.route.list_x[-1] >= house.route.battery.position_x:
            horizontal = - 1
        # else increase x-coordinate
        else:
            horizontal = 1

        # if house is further on y-axis than battery: decrease y-coordinate
        if house.route.list_y[-1] > house.route.battery.position_y:
            vertical = -1
        # else increase y-coordinate
        else:
            vertical = 1

        return horizontal, vertical


    def assign_battery(self, house):
        """
        assigns a battery to a house with the least distance between them

        house: House class

        Returns: None
        """

        # initiate variable to save coupled battery
        battery_chosen = None

        # save shortest distance in best, start with longest possible
        best = self.grid.grid_height + self.grid.grid_width + 2

        # loop through batteries
        for battery in self.grid.batteries:

            # calculate distance between x-coordinates + distance between y-coordinates from house to battery
            distance = abs(battery.position_x - house.position_x) + abs(battery.position_y - house.position_y)

            # if this is shorter than for last battery:
            if distance < best:

                # update best to shorter distance
                best = distance

                # set this battery as coupled battery
                battery_chosen = battery
        
        # Create Route class for house/battery couple
        house.route = Route(battery_chosen, house.position_x, house.position_y)

        # append house to list of connected houses for battery       
        battery_chosen.add_house(house)

        # update remaining capacity for battery
        battery_chosen.update_remaining(house, "subtract")

        return

    # https://www.programiz.com/python-programming/methods/list/sort
    def bubbleSort(arr, object):
        """
        sorts a list using bubble sort

        arr: list

        Returns: list
        """

        n = len(arr)

        # Traverse through all array elements
        for i in range(n-1):

            # Last i elements are already in place
            for j in range(0, n-i-1):

                # Swap if the element found is greater
                if object == "house":
                    if arr[j].max_output < arr[j + 1].max_output :
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                else:
                    if arr[j].remaining > arr[j + 1].remaining :
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]

        return arr
        
    def track_shared(self, x, y, axis, direction):
        if axis == "x":
            if direction == 1:
                matrix = self.matrices["right"]
            else:
                matrix = self.matrices["left"]
        else:
            if direction == 1:
                matrix = self.matrices["up"]
            else:
                matrix = self.matrices["down"]

        if matrix[y][x] != 1:
            matrix[y][x] = 1
            
        return

    def lay_cables(self, house, horizontal, vertical):
        """
        Lays cables from house to battery and adds the coordinates to route class.
        Starts by going horizontal, then vertical until battery is reached.
        house: House class; 
        horizontal: int; 
        vertical: int

        Returns: None
        """
        
        # save non-chosen batteries in list
        other_batteries = []
        for battery in self.grid.batteries:
            if battery != house.route.battery:
                other_batteries.append(battery)
    
        # loop till x-coordinate of cable matches x-coordinate of battery
        while house.route.list_x[-1] != house.route.battery.position_x:

            # when house is not coupled to closest battery
            if house.check == True:
                axis = "x"

                # check if path doesn't cross other batteries
                self.bypass_battery(house, horizontal, vertical, axis, other_batteries)

                # re-calculate direction from path to battery
                horizontal, vertical = self.define_direction(house)
            else:
                x = house.route.list_x[-1] + horizontal
                y = house.route.list_y[-1]
                
                house.route.list_x.append(x)
                house.route.list_y.append(y)

                # add cables to matrix
                self.track_shared(x, y, "x", horizontal)

        # loop till y-coordinate of cable matches y-coordinate of battery
        while house.route.list_y[-1] != house.route.battery.position_y:

            # when house is not coupled to closest battery
            if house.check == True:
                axis = "y"

                # check if path doesn't cross other batteries
                self.bypass_battery(house, horizontal, vertical, axis, other_batteries)

                # re-calculate direction from path to battery
                horizontal, vertical = self.define_direction(house)
            else:
                y = house.route.list_y[-1] + vertical
                x = house.route.list_x[-1]

                house.route.list_y.append(y)
                house.route.list_x.append(x)
                
                # add cables to matrix
                self.track_shared(x, y, "y", vertical)

        # set checking back to
        house.check = False

        return

    def bypass_battery(self, house, horizontal, vertical, axis, other_batteries):
        """
        bypasses battery if house is relocated and needed

        house: House class; 
        horizontal: int; 
        vertical: int;
        axis: string
        other_batteries: list

        returns: None
        """
        x = house.route.list_x[-1]
        y = house.route.list_y[-1]
  
        # print(house)

        # check if new coordinated don't lead to other batteries
        for battery in other_batteries:
            # print(battery)
              
            # if path is moving across the x-axis
            if axis == "x":
                
                # bypass other batteries 
                if x + horizontal == battery.position_x and y == battery.position_y:

                    # Move one y-coordinate up or down, then one x coordinate left or right depending on direction towards right battery
                    house.route.list_x.extend([x, x + horizontal])
                    house.route.list_y.extend([y + vertical, y + vertical])

                    # add cables to matrix
                    self.track_shared((x + horizontal), ( y + vertical), "x", horizontal)
                    self.track_shared(x, (y + vertical), "y", vertical)
                    return
            # bewegen over de y-as
            else:

                # bypass other batteries 
                if x == battery.position_x and y + vertical == battery.position_y:

                    # Move one x coordinate left or right, then one y-coordinate up or down depending on direction towards right battery
                    house.route.list_x.extend([x + horizontal, x + horizontal])
                    house.route.list_y.extend([y, y + vertical])

                    # add cables to matrix
                    self.track_shared((x + horizontal), y, "x", horizontal)
                    self.track_shared((x + horizontal), (y + vertical), "y", vertical)
                    return

        # append if bypasses is not needed
        if axis == "x":
            
            # changes x coordinate
            house.route.list_x.append(x + horizontal)
            house.route.list_y.append(y)

            # add cables to matrix
            self.track_shared((x + horizontal), y, "x", horizontal)
        else:

            # changes y coordinate
            house.route.list_x.append(x)
            house.route.list_y.append(y + vertical)
            
            # add cables to matrix
            self.track_shared(x, (y + vertical), "y", vertical)
        return