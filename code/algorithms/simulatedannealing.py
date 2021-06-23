"""
Created by CodeName

This file contains a Simulated Annealing class
"""

import random

class Simulated_Annealing():
    """
    Simulated Annealing algorithm.

    Extension on Hill climber with decreasing temperature included in the probability function
    """

    def __init__(self, start_temperature, iterations):
        self.start_temperature = start_temperature
        self.iterations = iterations
        self.temperature = 1

        
    def update_temperature(self, cooling_scheme, i):
        """
        Update temperature using either exponential or linear function.

        Returns: Temperature
        """
        
        if cooling_scheme == "exp":

            # Exponential function
            self.temperature = self.start_temperature * (0.999 ** i)
        else:

            # Lineair function
            self.temperature = self.start_temperature - (self.start_temperature / self.iterations) * i

        return self.temperature

    def check(self, old_state, new_state, temperature):
        """
        Calculates the cost of previous and new state. 
        Then calculates the acceptance probability incorporating temperature. 
        Uses random number between 0 & 1 to accept worse new states at times.

        old_state: Grid class
        new_state: Grid class

        Returns: Grid class, int
        """

        costs_old = old_state.shared_costs()
        costs_new = new_state.shared_costs()

        # From: Minor Programmeren, Programmeertheorie, Iteratieve Algoritme - Bas Terwijn
        probability = 2 ** ((costs_old - costs_new) / temperature )

        if random.random() < probability:

            # Accept new state
            return new_state, costs_new
        else:

            # Accept old state
            return old_state, costs_old
