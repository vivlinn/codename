class Route():
    def __init__(self, battery):
        self.battery = battery
        self.list_x = []
        self.list_y = []

    def length(self):
        price = len(self.list_x) * 9
        return price
        