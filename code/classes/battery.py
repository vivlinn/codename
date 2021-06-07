class Battery():
    def __init__(self, id, position_x, position_y, capacity):
        self.id = id
        self.capacity = capacity
        self.remaining = self.capacity
        self.position_x = position_x
        self.position_y = position_y
        # self.price = price
