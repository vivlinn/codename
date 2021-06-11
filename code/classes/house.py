class House():
    def __init__(self, id, max_output, position_x, position_y):
        self.id = id
        self.max_output = max_output
        self.position_x = position_x
        self.position_y = position_y
        self.route = None
        self.check = False
        # self.price = price
        