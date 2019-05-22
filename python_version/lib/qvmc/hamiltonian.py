import numpy as np
import random
import math
from matplotlib import pyplot as plt
from math import exp
import time
import cmath

from pdb import set_trace

class Hamiltonian:
    def __init__(self, num_particles, delta = 0.0):
        self.num_particles = num_particles
        self.delta = delta

        self.debug = False

    def calculate_local_energy(self, state):
        """
        This function calculates the local energy of a state
        """
        config = state.configuration
        # print(f"State for calc local energy: {state}")
        # contribution from Z direction spin terms
        energy = 0
        state_proj = state.get_variational_projection()

        for i in range(self.num_particles):
            energy += (1-self.delta*pow(-1, i + 1))*(state_proj*config[i] * config[(i+1) % self.num_particles])/4
        diagonal_energies = energy

        # contributions from off diagonal terms
        non_diagonal_energies = 0
        off_diag_states = state.get_off_diagonal_configurations() # tuple of (switch position , state)
        for i, state in off_diag_states:
            non_diagonal_energies += (1-self.delta*pow(-1, i+1))*(-0.5)*state.get_variational_projection()
        energy += non_diagonal_energies

        return energy / state_proj
