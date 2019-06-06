#!python
#cython: language_level=3

import numpy as np
import random
import math
from IPython.display import clear_output
from math import exp
import time
import cmath

from pdb import set_trace

class State:
    def __init__(self, num_particles, variational_parameters, configuration = None):

        self.num_particles = num_particles
        self.parameters = variational_parameters # dictionary of variational param data strctures

        # inialize these to None. Only calulate if need be
        self.off_diagonal_configurations = None
        self.coefficient = None
        self.delta_x = None
        self.Q_of_x = None

        if configuration is None:
            self.randomize_state()
        else:
            self.configuration = configuration

    def randomize_state(self):
        state = []
        N = self.num_particles
        positive_positions = random.sample(range(0, N - 1), int(N/2))
        for i in range(N):
            if i in positive_positions:
                state.append(1)
            else:
                state.append(-1)
        self.configuration = np.asarray(state)

    def generate_coefficient(self):
        """
        This function generates the variational
        projection for this particular state.
        """
        N = self.num_particles
        w = self.parameters["w"]

        config = self.configuration
        try:
            exponential = 0
            coefficient = 1

            # determine exponetial contribution (all real parameters)
            for i, param in enumerate(self.parameters["a"]):
                exponential += param*config[i]

            coefficient *= cmath.exp(exponential)

            # determine contribution from hyperbolic cosines
            for i, param in enumerate(self.parameters["b"]):
                cosh_arg = param
                for j in range(N):
                    try:
                        cosh_arg += config[j]*w[i][j]
                    except:
                        print("TRY ERROR in state.pyx")
                        print(config)
                        print(w)
                        
                coefficient*= cmath.cosh(cosh_arg)

            self.coefficient = coefficient

        except OverflowError:
            print(f"Error: Overflow. State = {config}   alpha = {self.parameters}")

    def generate_off_diagonal_configurations(self):
        """
        This function generates a list of configurations that could
        be flipped into the inputted by state by the application of
        Raising or lowering operators (Check the hamiltonian equation)

        returns a list of configurations

        ***NOTE: This solution is computationally intractable and might not
        be the most optimal one

        """
        config_copy = self.configuration.copy()
        config = self.configuration

        off_diagonal_configurations = list()
        switch_positions = list() # list of indices where the flip occured
        for i in range(len(config)):
            if i == self.num_particles - 1:
                if config[i] != config[0]:
                    config_copy[i] *= -1
                    config_copy[0] *= -1
                    off_diagonal_configurations.append((i, State(self.num_particles,
                                self.parameters, configuration = config_copy)))
                del config_copy # I think numpy does this automatically but just in case
                self.off_diagonal_configurations = off_diagonal_configurations
                return
            if config[i] != config[i+1]:
                config_copy[i] *= -1
                config_copy[i+1] *= -1
                off_diagonal_configurations.append((i,State(self.num_particles,
                                self.parameters, configuration = config_copy)))
                config_copy = config.copy()

    def get_off_diagonal_configurations(self):
        if not self.off_diagonal_configurations:
            self.generate_off_diagonal_configurations()
        return self.off_diagonal_configurations

    def get_variational_projection(self):
        if not self.coefficient:
            self.generate_coefficient()
        return self.coefficient

    def clear_state(self):
        self.off_diagonal_configurations = None
        self.coefficient = None
        self.delta_x = None
        self.Q_of_x = None

    def update_state(self):

        def random_flip(config):
            """
            Input is a state configuration -- (numpy array)

            Randomly flips two bits of a state such
            that there are still two up and two down
            """
            choices = random.sample(list(range(0,self.num_particles)), self.num_particles)
            flip1_index = choices.pop()
            flip1_value = config[flip1_index]
            config[flip1_index] *= -1
            cont = True
            while(cont):
                flip2_index = choices.pop()
                if config[flip2_index] != flip1_value:
                    config[flip2_index] *= -1
                    cont = False
            return State(self.num_particles, self.parameters, configuration = config)

        def compute_R(trial_state):
            """
            Function compute "R", which is the ratio between the weight functions
            of the initial state and the trial state.
            """
            a = trial_state.get_variational_projection()
            b = self.get_variational_projection()

            numerator = a * a.conjugate()
            denominator = b * b.conjugate()

            if denominator.real < numerator.real:
                return 2.0
            return numerator.real / denominator.real

        trial_state = random_flip(self.configuration.copy())
        R = compute_R(trial_state)
        r = random.uniform(0,1)
        if R > r:
            self.clear_state()
            self.configuration = trial_state.configuration
            self.coefficient = trial_state.coefficient

    def calculate_delta_x(self):
        """
        This function gives the delta vector for a particular
        state. The delta vector is a vector with the derivative
        of the wave function with respect to the particular
        indexed paramater. The len the vector is the
        number of particles - 1 which the number of
        variational paramters.
        args:
        state - number array length N
        return:
        - delta_x : array length N-1 fo derivatives
        """

        config = self.configuration
        N = self.num_particles

        # for computational efficiency we will calculate this once
        w = self.parameters["w"]
        tanhs = np.zeros(self.num_particles, dtype=complex)

        # loop through all is and js. Calculate tanhs
        for i, param in enumerate(self.parameters["b"]):
                tanh_arg = param
                for j in range(N):
                    try:
                        tanh_arg += config[j]*w[i][j]
                    except:
                        print("TRY ERROR in state.pyx")
                        print(config)
                        print(w)
                        
                tanhs[i] = cmath.tanh(tanh_arg)

        delta_a = self.configuration
        delta_b = tanhs

        s = np.broadcast_to(config, (N,N))
        tanhs = np.broadcast_to(tanhs, (N,N)).T # broadcast tanhs and transpose

        delta_w = np.multiply(tanhs, s) # element wise multiplication
        # this should give you w[i][j] where i corresponds to the tanh and j corresponds to sj

        self.delta_x = {"a" : np.conjugate(delta_a), "b" : np.conjugate(delta_b), "w" : np.conjugate(delta_w) }


    def get_delta_x(self):
        if self.delta_x is None:
            self.calculate_delta_x()
        return self.delta_x

    def get_Q_of_x(self, energy):
        delta_x = self.get_delta_x()
        Q = dict()
        for key, value in delta_x.items():
            Q[key] = energy*value.copy()
        return Q
