"""
Created by CodeName.

This file contains a hill climber algorithm.

"""

# Importfiles
from code.algorithms.simulatedannealing import Simulated_Annealing
from .greedy import Greedy
from .randomize import Randomize
from code.classes.route import Route

# Importfunctions
import copy
import random

# Global variable
SAME_RESULT_STOP = 1000


class Hill_Climber():
    """
    HillClimber algorithm.
    Uses function from Random class to assign all houses to batteries for the start state.
    Then lays paths using create paths function from Greedy class.

    The algorithm rearranges houses over batteries and relays paths.

    Then compares start state with new arranged state and uses an acceptance change to keep the "best" state.
    Stops after N iterations or N repeated outcomes.

    Returns: Grid class
    """

    def __init__(self, grid, iterations, start_temperature, cooling_scheme, algorithm_houses, algorithm_cables):
        self.grid = grid
        self.iterations = iterations
        self.start_temperature = start_temperature
        self.cooling_scheme = cooling_scheme
        self.algorithm_houses = algorithm_houses
        self.algorithm_cables = algorithm_cables
        self.temperature = 1
        self.outcomes = []

    def run(self):
        """
        Divided in two parts. 
        First part optimalises assigning houses to batteries. 
        Second part optimalises shared cables between houses and batteries.

        Returns: Grid class.
        """

        # Takes best result assigned houses to batteries
        old_state = self.optimal_houses()
    
        # Best result shared cables
        best_state = self.optimal_cables(old_state)
       
        return best_state

    def optimal_houses(self):
        """
        Optimalises assigning houses to battery.
        """

        # Get random valid start state
        old_state = self.start_state()

        for i in range(self.iterations):
            print(f"Iteration: {i}")

            # Start checking after N iterations
            if i > SAME_RESULT_STOP + 1:
                counter = 0

                # Check if last N outcomes are repeated
                for j in range(1, SAME_RESULT_STOP):
                    if self.outcomes[-1] == self.outcomes[-(1+j)]:
                        counter += 1
                    else:
                        break      

                # Save state if N outcomes are repeated
                if counter == SAME_RESULT_STOP - 1:
                    return old_state
            
            # Update temperature if needed
            if self.algorithm_houses == "SA" and self.temperature > 0.1:
                simulated = Simulated_Annealing(self.start_temperature, self.iterations)
                self.temperature = simulated.update_temperature(self.cooling_scheme, i)         

            # Make small mutation
            while True:
                output = self.mutate(old_state)

                # if mutation is valid
                if output[0]:
                    # save mutation
                    new_state = output[1]
                    break

            # Compare both states and accept best state
            if self.algorithm_houses == "SA" and self.temperature > 0.1:
                old_state, costs = simulated.check(old_state, new_state, self.temperature)
                self.outcomes.append(costs)
            else:
                old_state = self.check(old_state, new_state)

        return old_state

    def optimal_cables(self, old_state):
        """
        Optimalises shared cables between houses and batteries.
        Here, the best state from optimal_houses will be used as start state.

        """
        self.outcomes = [] 
        
        # Get best house-state as start state
        for i in range(self.iterations):
            print(f"Iteration: {i}")

            # Start checking after N iterations
            if i > SAME_RESULT_STOP + 1:
                counter = 0

                # Check if last N outcomes are repeated
                for j in range(1, SAME_RESULT_STOP):
                    if self.outcomes[-1] == self.outcomes[-(1+j)]:
                        counter += 1
                    else:
                        break      

                # Save state if N outcomes are repeated
                if counter == SAME_RESULT_STOP - 1:
                    return old_state

            # Update temperature if needed
            if self.algorithm_cables == "SA" and self.temperature > 0.1:
                simulated = Simulated_Annealing(self.start_temperature, self.iterations)
                self.temperature = simulated.update_temperature(self.cooling_scheme, i)

            # Make small mutation
            new_state = self.mutate_cables(old_state)

            # Compare both states and accept best state
            if self.algorithm_cables == "SA" and self.temperature > 0.1:
                old_state, costs = simulated.check(old_state, new_state, self.temperature)
                self.outcomes.append(costs)
            else:
                old_state = self.check(old_state, new_state)

        return old_state

    def start_state(self):
        """
        Creates a start state using the Randomize class and keeps trying until a state is reached where all houses are coupled to batteries.

        Returns: Grid class.
        """

        while True:

            # Make copy
            grid_copy = copy.deepcopy(self.grid)

            # initialize random algorithm class
            random = Randomize(grid_copy)
            
            # Assign batteries randomly
            succes, grid_copy = random.assign_battery()
            
            # If resulting state is valid
            if succes == True:

                # Initialize greedy algorithm class
                greedy= Greedy(grid_copy)

                # Lay cables for all houses in the start state
                start_state = greedy.create_cables(grid_copy.houses)

                break

        return start_state  

    def mutate(self, old_state):
        """
        Adjusts the previous state by swapping 1 house per battery.

        old_state: Grid class.

        Returns: list; [Bool, Grid class].
        """

        # Make copy
        new_state = copy.deepcopy(old_state)

        # Initialize empty list for houses to be reassigned
        houses_left = []
        new_path = houses_left

        for battery in new_state.batteries:

            # Shuffle connected houses in random order
            random.shuffle(battery.connected_houses)

            # Remove house from battery
            house = battery.connected_houses.pop()

            # Set check at True again
            house.check = True
            
            greedy = Greedy(new_state)
            new_state = new_state.remove_shared(house)

            # Update remaining capacity
            battery.remaining += house.max_output

            # Add house to houses_left
            houses_left.append(house)

        # Shuffle houses
        random.shuffle(houses_left)

        for house in houses_left:

            # Loop until house is assigned to a battery
            while True:

                succes = False
                
                for battery in new_state.batteries:
                    
                    if house.max_output <= battery.remaining:
                        succes = True

                        break
                
                # Assign random battery to the house
                battery_chosen = random.choice(new_state.batteries)

                # Check if battery has capacity for the house
                if battery_chosen.remaining >= house.max_output:

                    # Update remaining chosen battery capacity
                    battery_chosen.remaining = battery_chosen.remaining - house.max_output
                    
                    break
                
                if succes == False:
                    return [succes, old_state]

            # Add route object to the house
            battery_chosen.connected_houses.append(house)
            house.route = Route(battery_chosen, house.get_x(), house.get_y())

        # Use greedy to lay cables for all reassigned houses
        greedy = Greedy(new_state)
        new_state = greedy.create_cables(new_path)
    
        return [succes, new_state]  
            
    def mutate_cables(self, old_state):
        """
        Adjusts the previous state by changing route of one house.

        old_state: Grid class.

        Returns: Grid class.
        """

        new_state = copy.deepcopy(old_state)
        
        # MAGIC NUMBER
        house_sample = random.sample(new_state.houses, 1)
        
        greedy = Greedy(new_state)

        for house in house_sample:
            
            new_state.remove_shared(house)
            
            house.route.list_x = [house.position_x, ]
            house.route.list_y = [house.position_y, ]

            # Set check at True again
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
        

    def check(self, old_state, new_state):
        """
        Calculates the cost of previous and new state. 
        Then calculates the acceptance probability incorporating temperature. 
        Uses random number between 0 & 1 to accept worse new states at times.

        old_state: Grid class
        new_state: Grid class

        Returns: Grid class
        """

        costs_old = old_state.shared_costs()
        costs_new = new_state.shared_costs()

        probability = 2 ** ((costs_old - costs_new))

        if random.random() < probability:
            # Accept new state
            self.outcomes.append(costs_new)
            return new_state
        else:
            # Accept old state
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
