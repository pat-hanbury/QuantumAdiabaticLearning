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
    def __init__(self, hamiltonian, config, delta, lr, iterations,
                 plotter = None, checkpoint_manager=None,
                 visdom_manager=None,
                 w_parameters = None, use_noise=True, 
                 fixed_parameters = None,
                 derivative_cap = 0.3):
        self.H = hamiltonian
        self.num_particles = hamiltonian.num_particles
        self.num_steps = config['num_steps']# number of steps for every monte carlo simulation
        self.lr = lr
        self.dx_cap = derivative_cap
        self.fixed_parameters = fixed_parameters
        self.monte_carlo_simulations_per_delta = iterations

        # quantities for calculating derivatives
        self.W_exp_Q = None #expectation of Q
        self.W_exp_delta = None # expectation of the delta array (also BIg Oh in sorrellas paper)
        self.variational_energy = None
        
        self.config = config
        
        self.convergence_indicator = config["convergence_indicator"]
        self.max_iter = iterations

        if w_parameters is None:
            self.randomize_parameters()
        else:
            self.w_parameters = w_parameters
            if (delta == 0.0) and use_noise:
                noise_scale = config['noise_scale']
                real_noise = np.random.normal(scale=noise_scale, size=w_parameters.shape)
                imag_noise = np.random.normal(scale=noise_scale, size=w_parameters.shape)*1j
                self.w_parameters = self.w_parameters+real_noise+imag_noise

        # some debugging features
        self.plotter = plotter
        self.checkpoint_manager = checkpoint_manager
        self.visdom_manager=visdom_manager
        self.debug = False
        self.sleep = False
        
    def update_LR(self, new_energy):
        if new_energy.real <= self.previous_energy.real:
            self.lr*= 1.1
            self.previous_parameters = self.w_parameters.copy()
            self.previous_energy = new_energy
            return True
        else:
            # if this happens, we reset and change the LR
            self.lr *= 0.6
            self.w_parameters = self.previous_parameters.copy()
            # self.update_variational_parameters()
            return False
            
        
        
    def update_variational_parameters(self):
        if self.variational_energy is None or self.W_exp_delta is None or self.W_exp_Q is None:
            print("OUT OF ORDER ERROR")
            set_trace()


        w_derivative_vector = 2*(self.W_exp_Q - self.W_exp_delta*self.variational_energy)
        w_parameter_changes = -1*self.lr*w_derivative_vector # FOO CHECK THIS
        cap = self.dx_cap + self.dx_cap*1j
        w_parameter_changes = w_parameter_changes.clip(-1*cap, cap)

        self.w_parameters = self.w_parameters + w_parameter_changes

        self.clear_expectations() # this insures we pick up more bugs
                
    def monte_carlo_simulation(self):
        """
        This function calculates expectation values for the
        4 variables of interest P, Q,
        """
        
        if self.config['Enumeration']:
            return self.enumeration_simulation()

        cdef int N = self.num_particles
        cdef int num_steps = self.num_steps
        cdef int i
        state = State(self.num_particles, self.w_parameters)

        # initialize running variables
        cdef complex expectation_local_energy = 0
        cdef complex local_energy
        expectation_delta =np.zeros(N)
        expectation_Q = np.zeros(N)

        for i in range(num_steps):
            # clear_output(wait=True)

            state.update_state()
            local_energy = self.H.calculate_local_energy(state)
            delta_x = state.get_delta_x()
            Q_of_x = state.get_Q_of_x(local_energy)

            expectation_local_energy += local_energy
            expectation_delta = expectation_delta + delta_x
            expectation_Q = expectation_Q + Q_of_x
            
        # normalize expectation values
        num_steps = self.num_steps
        expectation_local_energy = expectation_local_energy / num_steps
        expectation_delta = expectation_delta / num_steps
        expectation_Q = expectation_Q / num_steps
        
        return expectation_local_energy, expectation_delta, expectation_Q
    
    def enumeration_simulation(self):
        """
        This function calculates expectation values for the
        4 variables of interest P, Q,
        
        Using enumeration as a simulation technique instead of
        monte carlo
        """
        cdef int N = self.num_particles
        cdef int i
        state = State(self.num_particles, self.w_parameters)

        # initialize running variables
        cdef complex expectation_local_energy = 0
        cdef complex local_energy
        expectation_delta = np.zeros(N)
        expectation_Q = np.zeros(N)
        
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
            state = State(self.num_particles, self.w_parameters)
            state.configuration = permutation
            coeff = state.get_variational_projection()
            sum_squared_coefficients += coeff * coeff.conjugate()
            states.append(state)
            
        local_energies = []
        
        for state in states:
            coeff = state.get_variational_projection()
            squared_coefficient = coeff * coeff.conjugate()
            probability = squared_coefficient / sum_squared_coefficients
            
            local_energy = self.H.calculate_local_energy(state)
            delta_x = state.get_delta_x()
            Q_of_x = state.get_Q_of_x(local_energy)
            
            local_energies.append(local_energy*probability)
            
            
            expectation_local_energy += local_energy*probability
            expectation_delta = expectation_delta + delta_x*probability
            expectation_Q = expectation_Q + Q_of_x*probability
            
        local_energies = np.asarray(local_energies)
        energies_std = np.std(local_energies)
        relative_std = abs(energies_std / expectation_local_energy)
        
        return expectation_local_energy, expectation_delta, expectation_Q, relative_std        

    
    def clear_expectations(self):
        self.exp_Q = None
        self.varitional_enery = None
        self.exp_delta = None
        
    def get_ground_state(self):

        # def check_ending_conditions()

        # pre loop conditions
        # cdef int i
        cdef complex min_energy = 99999999999
        cdef int time_caught_in_local_min = 0
        cdef int loop_count = 0
        cdef int total_loops = self.monte_carlo_simulations_per_delta
        
        cdef int reset_count = 0 # the number of times the alpha was randomly initialized
        
        relative_std = 1.0
        count = -1
        
        while(relative_std > self.convergence_indicator and (count < self.max_iter)):
            count+=1
            # print(f"Count: {count} Relative STD: {relative_std}")
            try:
                # clear_output(wait=True)

                self.variational_energy, self.W_exp_delta, self.W_exp_Q, relative_std = self.monte_carlo_simulation()
                
                if count == 0:
                    self.previous_energy = self.variational_energy
                    self.previous_parameters = self.w_parameters.copy()
                    update_parameters = True
                else:
                    update_parameters = self.update_LR(self.variational_energy)
                
                # print(f"var energy: {self.variational_energy} \ndelta: {self.exp_delta}\nQ: {self.exp_Q}")

                if self.plotter is not None:
                    self.plotter.update_history(self.variational_energy, self.w_parameters)
                    self.plotter.update_std_history(relative_std)
                    self.plotter.update_LR_history(self.lr)
                    if self.plotter.plot_real_time:
                        self.plotter.show_plot()
                # if this energy is lowest, update optimal measurements,
                # and assume you can do better (set end count, i, to zero)
                if self.variational_energy.real < min_energy.real:
                        min_energy = self.variational_energy
                        optimal_parameters = self.w_parameters.copy()
                        if self.checkpoint_manager is not None:
                            self.checkpoint_manager.save_checkpoint(optimal_parameters, count)
                if update_parameters:
                    self.update_variational_parameters()

                loop_count += 1
                if loop_count == total_loops:
                    # print("Ending because loop count == 50")
                    cont = False
            except KeyboardInterrupt:
                cont = False
                # print("Ending because Keyboard interruption")
        self.plotter.save_parameter_plot()
        if self.visdom_manager is not None:
            self.visdom_manager.update_energy_history(self.variational_energy)
        return min_energy, optimal_parameters, self.w_parameters
