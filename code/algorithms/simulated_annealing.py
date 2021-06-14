from main import ITERATIONS
from . import greedy, random
from code.classes.route import Route
import copy
import random

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
            mutate(start_state)
            check()

            # change temperature



    # START STATE
    def start_state(self):
        while True:

            grid_copy = copy.deepcopy(self.grid)

            succes = random.assign_battery(grid_copy)

            if succes == True:
                start_state = greedy.create_cables(grid_copy)
                break
            else:
                print(succes)

        return start_state

    def mutate(self, start_state):
        # itereren over batterijen
            # haal vijf random huizen eruit
            # stop deze in de lijst
        
        # itereer over lengte van de lijst
            # kies random huis uit lijst
                # itereer over batterijen
                    # koppel dit huis aan de batterij
                        # check of het is gelukt
                            # return false
        # return true

        old_state = copy.deepcopy(start_state)

        houses_left = []
        for battery in old_state.batteries:
            # shuffle connected houses in random order
            random.shuffle(battery.connected_houses)

            for i in range(5):
                # remove house from battery
                house = battery.connected_houses.pop()
                # update remaining capacity
                battery.remaining += house.max_output
                # add house to houses_left
                houses_left.append(house)


        random.shuffle(houses_left)
        for house in houses_left:
            # loop till a battery is assigned to a house
            while True:

                succes = False
                for battery in old_state.batteries:
                    if house.max_output <= battery.remaining:
                        succes = True
                        break
                

                # assign random battery to the house
                battery_chosen = random.choice(old_state.batteries)

                # check if battery has capacity for the house
                if battery_chosen.remaining >= house.max_output:

                    # update remaining battery_chosen capacity
                    battery_chosen.remaining = battery_chosen.remaining - house.max_output
                    break
                
                if succes == False:
                    return succes

            # add route object to the house
            battery_chosen.connected_houses.append(house)
            house.route = Route(battery_chosen, house.position_x, house.position_y)

