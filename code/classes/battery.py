class Battery():
    def __init__(self, id, position_x, position_y, capacity):
        self.id = id
        self.capacity = capacity
        self.remaining = self.capacity
        self.position_x = position_x
        self.position_y = position_y
        self.connected_houses = []
        # self.price = price

    def add_house(self, house):
        self.connected_houses.append(house)
        return
    
    def remove_house(self):
        house = self.connected_houses.pop()
        return house

    def update_remaining(self, house, change):
        if change == "add":
            self.capacity += house.max_output
        else:
            self.capacity -= house.max_output
        return