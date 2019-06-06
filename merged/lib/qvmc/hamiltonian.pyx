#!python
#cython: language_level=3

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
    def __init__(self, config, num_particles, is_final_hamiltonian, delta = 0.0):
        self.num_particles = num_particles
        self.delta = delta
        self.is_final_hamiltonian = is_final_hamiltonian # if true, will calculate a ring
        self.config = config

    def calculate_local_energy(self, state):
        if config['Algorithm'] == 'Algorithm_1':
            return self.apply_algo1_hamiltonian(state)
        elif config['Algorithm'] == 'Algorithm_2':
            return self.apply_algo2_hamiltonian(state)
        
    def apply_algo1_hamiltonian(self, state):
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
    
    
    def apply_algo2_hamiltonian(self, state):
        """
        This function calculates the local energy of a state
        """
        config = state.configuration
        # print(f"State for calc local energy: {state}")
        # contribution from Z direction spin terms
        cdef int N = self.num_particles
        cdef complex energy = 0
        cdef complex state_proj = state.get_variational_projection()
        cdef float delta = self.delta
        
        cdef int i

        for i in range(N):
            if (i == (int(N/2) - 1)) or ((i == (N-1)) and self.is_final_hamiltonian):
                energy += delta*(state_proj*config[i] * config[(i+1) % self.num_particles])/4
            elif (i == N-1): # this is if it's not the final hamiltonian -- we ignore the last interaction (chain)
                pass
            else:
                energy += (state_proj*config[i] * config[(i+1) % self.num_particles])/4
        diagonal_energies = energy

        # contributions from off diagonal terms
        non_diagonal_energies = 0
        off_diag_states = state.get_off_diagonal_configurations() # tuple of (switch position , state)
        
        for i, state in off_diag_states:
            if (i == (int(N/2) - 1)) or ((i == (N-1)) and self.is_final_hamiltonian):
                non_diagonal_energies += delta*(-0.5)*state.get_variational_projection()
            else:
                non_diagonal_energies += (-0.5)*state.get_variational_projection()
                
        energy += non_diagonal_energies

        return energy / state_proj
    