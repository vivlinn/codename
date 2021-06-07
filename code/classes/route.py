class Route():
    def __init__(self, id, list_x, list_y):
        self.id = id
        # self.battery = battery
        self.list_x = list_x
        self.list_y = list_y

    def length(self):
        price = len(self.list_x) * 9
        return price
        