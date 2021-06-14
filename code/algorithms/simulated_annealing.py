from main import ITERATIONS
from . import greedy, random
from code.classes.route import Route
import copy

# Herhaal:
    # Kies een random start state
    # Kies start temperatuur
    # Herhaal N iteraties:
        # Doe een kleine random aanpassing
        # Als random( ) > kans(oud, nieuw, temperatuur):
            # Maak de aanpassing ongedaan
        # Verlaag temperatuur

class simulated_annealing():

    def __init__(self, grid):
        self.grid = grid
        self.iterations = 100
        self.temperature = 1000


    def run(self):

        # KIES EEN START STATE
        start_state = self.start_state(self.grid)

        # KIES EEN TEMPERATUUR

        # HERHAAL N ITERATIES
        for i in range(self.iterations):
            mutate()
            check()

            # change temperature



    # START STATE
    def start_state(self):
        while True:

            grid_copy = copy.deepcopy(self.grid)

            succes = random.assign_battery(grid_copy)

            if succes == True:
                state = greedy.create_cables(grid_copy)
                break
            else:
                print(succes)


    def mutate(self):
        pass