class Battery():
    def __init__(self, id, position_x, position_y, capacity):
        self.id = id
        self.capacity = capacity
        self.remaining = self.capacity
        self.position_x = position_x
        self.position_y = position_y
        self.connected_houses = []

    def add_house(self, house):
        """
        Connect house to battery.
        """
        self.connected_houses.append(house)
        return
    
    def remove_house(self):
        """
        Disconnect house from battery.
        """
        house = self.connected_houses.pop()
        return house

    def update_remaining(self, house, change):
        """
        Change remaining capacity of battery.
        """
        if change == "add":
            self.capacity += house.max_output
        else:
            self.capacity -= house.max_output
        return