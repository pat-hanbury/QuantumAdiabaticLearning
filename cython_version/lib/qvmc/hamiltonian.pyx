import numpy as np
import random
import math
from matplotlib import pyplot as plt
from math import exp
import time
import cmath

from lib.qvmc.state import State

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
        cdef complex energy = 0
        cdef complex state_proj = state.get_variational_projection()
        cdef float delta = self.delta
        
        cdef int i

        for i in range(self.num_particles):
            # old hamiltonian
            # energy += (1-delta*pow(-1, i + 1))*(state_proj*config[i] * config[(i+1) % self.num_particles])/4
            if i % 2 == 0:
                energy += (state_proj*config[i] * config[(i+1) % self.num_particles])/4
            else:
                energy += delta*(state_proj*config[i] * config[(i+1) % self.num_particles])/4
        diagonal_energies = energy

        # contributions from off diagonal terms
        non_diagonal_energies = 0
        off_diag_states = state.get_off_diagonal_configurations() # tuple of (switch position , state)
        
        for i, state in off_diag_states:
            # old hamiltonian
            # non_diagonal_energies += (1-delta*pow(-1, i+1))*(-0.5)*state.get_variational_projection()
            if i % 2 == 0:
                non_diagonal_energies += (-0.5)*state.get_variational_projection()
            else:
                non_diagonal_energies += delta*(-0.5)*state.get_variational_projection()
        energy += non_diagonal_energies

        return energy / state_proj
