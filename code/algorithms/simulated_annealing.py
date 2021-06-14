from . import greedy, randomize
from code.classes.route import Route
from code.visualisation import costs

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
        self.start_temperature = 1000
        self.temperature = 0


    def run(self):

        # KIES EEN START STATE
        old_state = self.start_state()

        # KIES EEN TEMPERATUUR

        # HERHAAL N ITERATIES
        for i in range(self.iterations):
            # change temperature
            self.temperature = self.start_temperature - (self.start_temperature / self.iterations) * i
            # make mutations
            new_state = self.mutate(old_state)
            # compare states and accept best state
            old_state = self.check(old_state, new_state)

        return old_state    
            

    # START STATE
    def start_state(self):
        while True:

            grid_copy = copy.deepcopy(self.grid)

            succes = randomize.assign_battery(grid_copy)

            if succes == True:
                start_state = greedy.create_cables(grid_copy, grid_copy.houses)
                break
            else:
                print(succes)

        return start_state

    def mutate(self, old_state):
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

        new_state = copy.deepcopy(old_state)

        houses_left = []
        new_path = houses_left
        for battery in new_state.batteries:
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
                for battery in new_state.batteries:
                    if house.max_output <= battery.remaining:
                        succes = True
                        break
                

                # assign random battery to the house
                battery_chosen = random.choice(new_state.batteries)

                # check if battery has capacity for the house
                if battery_chosen.remaining >= house.max_output:

                    # update remaining battery_chosen capacity
                    battery_chosen.remaining = battery_chosen.remaining - house.max_output
                    break
                
                if succes == False:
                    break

            # add route object to the house
            battery_chosen.connected_houses.append(house)
            house.route = Route(battery_chosen, house.position_x, house.position_y)


        greedy.create_cables(new_state, new_path)


    def check(self, old_state, new_state):
        print()
        print(old_state)
        print(new_state)

        costs_old = costs.get_costs(old_state)
        costs_new = costs.get_costs(new_state)

        probability = 2 ** ((costs_old - costs_new) / self.temperature)

        if random.random() < probability:
            # accept new state
            return new_state
        else:
            # accept old state
            return old_state
