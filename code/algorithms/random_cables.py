from random import random
from classes.route import Route
import queue
import copy

def random_cables(grid):
    for house in grid.houses:
        if True:
            battery = random.choice(grid.batteries)
            if battery.remaining >= house.max_output:
                break

        house.route = Route(battery)

        depth = 20
        


depth = 3
queue = queue.Queue()
queue.put("")
while not queue.empty():
    state = queue.get()
    print(state)
    if len(state) < depth:
        for i in [ '1', '2']:
            child = copy.deepcopy(state)
            child += i
            queue.put(child)