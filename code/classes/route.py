class Route():
    def __init__(self, battery, x, y):
        self.battery = battery
        self.list_x = [x,]
        self.list_y = [y,]

    def length(self):
        price = len(self.list_x) * 9
        return price
        