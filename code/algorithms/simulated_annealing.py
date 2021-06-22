from main import SIZE_GRID
from .greedy import Greedy
from .randomize import Randomize
from code.classes.route import Route
from code.visualisation import costs

import copy
import random


SAME_RESULT_HOUSES = 1000
SAME_RESULT_CABLES = 1000
ALGORITHM_HOUSES = "HC"
ALGORITHM_CABLES = "SA"

class Simulated_annealing():
    """
    Simulated annealing algorithm.
    Uses function from Random class to assign all houses to batteries for the start state.
    Then lays paths using create paths function from Greedy class.

    The algorithm rearranges houses over batteries and relays paths.

    Then compares start state with new arranged state and uses an acceptance change to keep the "best" state. Stops after n iterations.

    Returns: Grid class
    """

    def __init__(self, grid, iterations, start_temperature):
        self.grid = grid
        self.iterations = iterations
        self.start_temperature = start_temperature
        self.temperature = 1
        self.outcomes = []

    def run(self):
        """
        Main function; first creates a start state, then loops n times to create a new state(Keeps trying until a state is reached where all houses are coupled to batteries.), compares their costs and accepts the best state.

        Returns: Grid class
        """

        # Best result from running algorithm
        old_state = self.optimal_houses()
    
        # Best result shared cables
        best_state = self.optimal_cables(old_state)
       
        return best_state

    def optimal_houses(self):

        # Get random start state
        old_state = self.start_state()

        # loop N times
        for i in range(self.iterations):
            print(i)

            # start checking after 100 iterations
            if i > SAME_RESULT_HOUSES + 1:
                counter = 0

                # check if last 20 outcomes are the same
                for j in range(1, SAME_RESULT_HOUSES):
                    if self.outcomes[-1] == self.outcomes[-(1+j)]:
                        counter += 1
                    else:
                        break      

                # if last N are the same
                if counter == SAME_RESULT_HOUSES - 1:
                    return old_state

            # change temperature
            # ------------------------------------------- EXPONENTIAL ---------------------------------------------- #
            # self.temperature = self.start_temperature * (0.999 ** i)
            # ------------------------------------------- EXPONENTIAL ---------------------------------------------- #

            # --------------------------------------------- LINEAIR ------------------------------------------------ #
            # self.temperature = self.start_temperature - (self.start_temperature / self.iterations) * i
            # --------------------------------------------- LINEAIR ------------------------------------------------ #            

            # make small mutations
            while True:
                output = self.mutate(old_state)
                
                if output[0] == True:
                    new_state = output[1]
                    break
        
            # compare states and accept best state
            old_state = self.check(old_state, new_state, ALGORITHM_HOUSES)

        return old_state
            

    def optimal_cables(self, old_state):
        self.outcomes = [] 
        
        # Get best house-state as start state

        # loop N times
        for i in range(self.iterations):
            print(i)

            # start checking after 100 iterations
            if i > SAME_RESULT_CABLES + 1:
                counter = 0

                # check if last 20 outcomes are the same
                for j in range(1, SAME_RESULT_CABLES):
                    if self.outcomes[-1] == self.outcomes[-(1+j)]:
                        counter += 1
                    else:
                        break      

                # if last N are the same
                if counter == SAME_RESULT_CABLES - 1:
                    return old_state

            # change temperature
            # ------------------------------------------- EXPONENTIAL ---------------------------------------------- #
            self.temperature = self.start_temperature * (0.999 ** i)
            
            # ------------------------------------------- EXPONENTIAL ---------------------------------------------- #

            # --------------------------------------------- LINEAIR ------------------------------------------------ #
            # self.temperature = self.start_temperature - (self.start_temperature / self.iterations) * i
            # --------------------------------------------- LINEAIR ------------------------------------------------ #            

            # make small mutations
            new_state = self.mutate_cables(old_state)            
            
            # compare states and accept best state
            old_state = self.check(old_state, new_state, ALGORITHM_CABLES)
            
        return old_state

    # START STATE
    def start_state(self):
        """
        Creates a start state using the Randomize class and keeps trying until a state is reached where all houses are coupled to batteries.

        Returns: Grid class
        """

        while True:

            grid_copy = copy.deepcopy(self.grid)
            
            grid = Randomize(grid_copy)
            succes, grid_copy = grid.assign_battery(grid_copy)
            
            if succes == True:

                grid= Greedy(grid_copy)
                start_state = grid.create_cables(grid_copy.houses)

                break

        return start_state  

    def mutate(self, old_state):
        """
        adjusts the previous state by swapping 5 houses per battery.

        old_state: Grid class 

        Returns: list; [Bool, Grid class]
        """

        new_state = copy.deepcopy(old_state)

        houses_left = []
        new_path = houses_left

        for battery in new_state.batteries:

            # shuffle connected houses in random order
            random.shuffle(battery.connected_houses)

            for i in range(1):
                # remove house from battery
                house = battery.connected_houses.pop()

                # set check at True again
                house.check = True

                greedy = Greedy(new_state)
                new_state = new_state.remove_shared(house)

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
                    return [succes, old_state]

            # add route object to the house
            battery_chosen.connected_houses.append(house)
            house.route = Route(battery_chosen, house.position_x, house.position_y)

        greedy = Greedy(new_state)
        new_state = greedy.create_cables(new_path)
    
        return [succes, new_state]  
            
    def mutate_cables(self, old_state):
        new_state = copy.deepcopy(old_state)
        
        # MAGIC NUMBER
        house_sample = random.sample(new_state.houses, 1)
        
        greedy = Greedy(new_state)

        for house in house_sample:
            
            new_state.remove_shared(house)
            
            house.route.list_x = [house.position_x, ]
            house.route.list_y = [house.position_y, ]

            # set check at True again
            house.check = True

            while True:
                move = random.randint(-10, 10)

                if house.position_y + move > 0 and house.position_y + move < self.grid.height:
                    break

            if move < 0:
                tmp = -1 
            else:
                tmp = 1

            if move != 0:
                for i in range(abs(move)):
                    house.route.list_x.append(house.position_x)
                    house.route.list_y.append(house.route.list_y[-1] + tmp)
                    
                    new_state.track_shared(house.position_x, house.route.list_y[-1], "y", tmp)
        
        new_state = greedy.create_cables(house_sample)
       
        return new_state
        

    def check(self, old_state, new_state, type):
        """
        Calculates the cost of previous and new state. 
        Then calculates the acceptance probability incorporating temperature. 
        Uses random number between 0 & 1 to accept worse new states at times.

        old_state: Grid class
        new_state: Grid class

        Returns: Grid class
        """

        costs_old = costs.shared_costs(old_state)
        costs_new = costs.shared_costs(new_state)

        if type == "HC" or self.temperature < 0.1:
            probability = 2 ** ((costs_old - costs_new))
        else:
            probability = 2 ** ((costs_old - costs_new) / self.temperature )
            print()
            print(self.temperature)
            print(probability)

        if random.random() < probability:
            # accept new state
            self.outcomes.append(costs_new)
            return new_state
        else:
            # accept old state
            self.outcomes.append(costs_old)
            return old_state


    def plot(self):
        """
        Gets both the costs of all inbetween states, and a range of 0 to the number of iterations of the algorithm as lists.

        Returns: list of lists

        """
        y_axis = self.outcomes
        
        x_axis = range(0,len(self.outcomes))

        return x_axis, y_axis
