#!python
#cython: language_level=3

import numpy as np
import random
import math
from matplotlib import pyplot as plt
from IPython.display import clear_output
from math import exp
import time
import cmath

from tqdm import tqdm

from .state import State
from .hamiltonian import Hamiltonian

from pdb import set_trace

class Optimizer:
    def __init__(self, hamiltonian, num_steps, cfg,
                 plotter = None, parameters = None, fixed_parameters = None,
                 lr = 0.03, derivative_cap = 0.3, random_noise_scale = None):
        self.H = hamiltonian
        self.num_particles = hamiltonian.num_particles
        self.num_steps = num_steps# number of steps for every monte carlo simulation
        self.lr = lr # learning rate
        self.dx_cap = derivative_cap
        self.fixed_parameters = fixed_parameters
        self.monte_carlo_simulations_per_delta = cfg['num_monte_carlos_per_delta']

        # quantities for calculating derivatives
        self.exp_Q = None #expectation of Q
        self.exp_delta =None # expectation of the delta array (also BIg Oh in sorrellas paper)
        self.variational_energy = None

        if parameters is None:
            self.randomize_parameters()
        else:
            self.parameters = parameters
            if random_noise_scale is not None:
                for key, value in self.parameters.items():
                    real_noise = np.random.normal(scale=random_noise_scale, size=value.shape)
                    imag_noise = np.random.normal(scale=random_noise_scale, size=value.shape)*1j
                    self.parameters.update({key : value+real_noise+imag_noise})
                # self.add_noise()

        # some debugging features
        self.plotter = plotter
        self.debug = False
        self.sleep = False

    def randomize_parameters(self):
        print("ERROR: RANDOMIZED PARAMETERS NOT DEFINED")
        set_trace()

    def update_variational_parameters(self):
        if self.variational_energy is None or self.exp_delta is None or self.exp_Q is None:
            print("OUT OF ORDER ERROR")
            set_trace()

        f = {}
        f.update((key, None) for key in self.parameters.keys())
        parameter_changes = {}
        for key in self.parameters.keys():
            f[key] = (self.exp_Q[key] - self.exp_delta[key]*self.variational_energy) # derivative vector
            parameter_changes[key] = self.lr*f[key]
            cap = self.dx_cap + self.dx_cap*1j
            parameter_changes[key] = parameter_changes[key].clip(-1*cap, cap)
        
        try:
            for key in self.parameters.keys():
                self.parameters[key] = self.parameters[key] - parameter_changes[key]
        except:
            print('TRY error opt.py')
            print(self.parameters)
            print(parameter_changes)

        self.clear_expectations() # this insures we pick up more bugs

        # artificially contrain certain parameters
        if self.fixed_parameters is not None:
            for idx, param in self.fixed_parameters.items():
                self.parameters[idx] = param


    def monte_carlo_simulation(self):
        """
        This function calculates expectation values for the
        4 variables of interest P, Q,
        """

        cdef int N = self.num_particles
        cdef int i
        state = State(self.num_particles, self.parameters)

        # initialize running variables
        cdef complex expectation_local_energy = 0
        cdef complex local_energy
        cdef dict expectation_delta = {"a" : np.zeros(N), "b" : np.zeros(N), "w" : np.zeros(N)}
        cdef dict expectation_Q = {"a" : np.zeros(N), "b" : np.zeros(N), "w" : np.zeros(N)}
        
        def get_all_states(num_particles):
            initial_string = []

            def get_other_states(input_state , num_particles):
                if len(input_state) == num_particles:
                    return [input_state]
                elif sum(input_state) == int(num_particles/2):
                    return [input_state + [0 for i in range(num_particles - len(input_state))]]
                elif (len(input_state)- sum(input_state)) == int(num_particles/2):
                    return [input_state + [1 for i in range(num_particles - len(input_state))]]
                else:
                    return get_other_states(input_state + [0], num_particles) + get_other_states(input_state + [1], num_particles)


            return get_other_states([0], num_particles) + get_other_states([1], num_particles)
        
        permutations = np.asarray(get_all_states(N))
        permutations= permutations*2 - 1
        states  = []
        sum_squared_coefficients = 0
        
        for permutation in permutations:
            state = State(self.num_particles, self.parameters)
            state.configuration = permutation
            coeff = state.get_variational_projection()
            sum_squared_coefficients += coeff * coeff.conjugate()
            states.append(state)
        
        for state in states:
            coeff = state.get_variational_projection()
            squared_coefficient = coeff * coeff.conjugate()
            probability = squared_coefficient / sum_squared_coefficients
            
            local_energy = self.H.calculate_local_energy(state)
            delta_x = state.get_delta_x()
            Q_of_x = state.get_Q_of_x(local_energy)
            
            
            expectation_local_energy += local_energy*probability
            expectation_delta.update((key, value + delta_x[key]*probability) for key, value in expectation_delta.items())
            expectation_Q.update((key, value + Q_of_x[key]*probability) for key, value in expectation_Q.items())
        
        return expectation_local_energy, expectation_delta, expectation_Q               
                        

    def clear_expectations(self):
        self.exp_Q = None
        self.variational_energy = None
        self.exp_delta = None


    def get_ground_state(self):

        # def check_ending_conditions()

        # pre loop conditions
        cdef int i
        cdef complex min_energy = 99999999999
        cdef int time_caught_in_local_min = 0
        cdef int loop_count = 0
        cdef int total_loops = self.monte_carlo_simulations_per_delta
        
        cdef int reset_count = 0 # the number of times the alpha was randomly initialized
        for i in range(total_loops):
            try:
                # clear_output(wait=True)

                self.variational_energy, self.exp_delta, self.exp_Q = self.monte_carlo_simulation()
                # print(f"var energy: {self.variational_energy} \ndelta: {self.exp_delta}\nQ: {self.exp_Q}")

                if self.plotter is not None:
                    self.plotter.update_history(self.variational_energy, self.parameters)
                    if self.plotter.plot_real_time:
                        self.plotter.show_plot()
                # if this energy is lowest, update optimal measurements,
                # and assume you can do better (set end count, i, to zero)
                if self.variational_energy.real < min_energy.real:
                        min_energy = self.variational_energy
                        optimal_parameters = {}
                        # value is numpy array so each array needs to be copied so it doesn't share memory with self.parameters
                        optimal_parameters.update((key, value.copy()) for key, value in self.parameters.items())


                self.update_variational_parameters()

                loop_count += 1
                if loop_count == total_loops:
                    # print("Ending because loop count == 50")
                    cont = False
            except KeyboardInterrupt:
                cont = False
                # print("Ending because Keyboard interruption")
        self.plotter.save_parameter_plot()
        return min_energy, optimal_parameters, self.parameters
