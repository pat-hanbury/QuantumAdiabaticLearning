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

from pdb import set_trace

class Optimizer:
    def __init__(self, hamiltonian, num_steps, num_parameters,
                 plotter = None, parameters = None, fixed_parameters = None,
                 lr = 0.03, derivative_cap = 0.3, random_noise_scale = None):
        self.H = hamiltonian
        self.num_particles = hamiltonian.num_particles
        self.num_steps = num_steps# number of steps for every monte carlo simulation
        self.lr = lr # learning rate
        self.dx_cap = derivative_cap
        self.fixed_parameters = fixed_parameters

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
            f[key] = -1*(self.exp_Q[key] - self.exp_delta[key]*self.variational_energy)
            parameter_changes[key] = self.lr*f[key]
            cap = self.dx_cap + self.dx_cap*1j
            parameter_changes[key] = parameter_changes[key].clip(-1*cap, cap)

        for key in self.parameters.keys():
            self.parameters[key] = self.parameters[key] + parameter_changes[key]

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

        N = self.num_particles

        state = State(self.num_particles, self.parameters)

        # initialize running variables
        expectation_local_energy = 0
        expectation_delta = {"a" : np.zeros(N), "b" : np.zeros(N), "w" : np.zeros(N)}
        expectation_Q = {"a" : np.zeros(N), "b" : np.zeros(N), "w" : np.zeros(N)}

        for i in range(self.num_steps):
            # clear_output(wait=True)

            state.update_state()
            local_energy = self.H.calculate_local_energy(state)
            delta_x = state.get_delta_x()
            Q_of_x = state.get_Q_of_x(local_energy)

            if self.sleep:
                time.sleep(5)

            expectation_local_energy += local_energy
            expectation_delta.update((key, value + delta_x[key]) for key, value in expectation_delta.items())
            expectation_Q.update((key, value + Q_of_x[key]) for key, value in expectation_Q.items())
        # normalize expectation values
        num_steps = self.num_steps
        expectation_local_energy = expectation_local_energy / num_steps
        expectation_delta.update((key, value/num_steps) for key, value in expectation_delta.items())
        expectation_Q.update((key, value/num_steps) for key, value in expectation_Q.items())
        return expectation_local_energy, expectation_delta, expectation_Q

    def clear_expectations(self):
        self.exp_Q = None
        self.varitional_enery = None
        self.exp_delta = None


    def get_ground_state(self):

        # def check_ending_conditions()

        # pre loop conditions
        cont = True
        min_energy = 99999999999
        latest_energy = min_energy
        time_caught_in_local_min = 0
        loop_count = 0

        reset_count = 0 # the number of times the alpha was randomly initialized
        for i in tqdm(range(50)):
            try:
                # clear_output(wait=True)

                self.variational_energy, self.exp_delta, self.exp_Q = self.monte_carlo_simulation()
                # print(f"var energy: {self.variational_energy} \ndelta: {self.exp_delta}\nQ: {self.exp_Q}")

                if self.plotter is not None:
                    self.plotter.update_history(self.variational_energy, self.parameters)
                    self.plotter.show_plot()
                # if this energy is lowest, update optimal measurements,
                # and assume you can do better (set end count, i, to zero)
                if self.variational_energy < min_energy:
                        min_energy = self.variational_energy
                        optimal_parameters = self.parameters

                if self.variational_energy < (latest_energy - 0.05):
                    latest_energy = self.variational_energy
                    time_caught_in_local_min = 0
                    loop_count = 0
                # if not, inncrement the end count. If you don't get better
                # after 400 tries, it's probably time to stop
                else:
                    time_caught_in_local_min += 1
                    if time_caught_in_local_min == 50:
                        print("Ending because caught in local min")
                        cont = False

                self.update_variational_parameters()

                loop_count += 1
                if loop_count == 50:
                    print("Ending because loop count == 50")
                    cont = False
            except KeyboardInterrupt:
                cont = False
                print("Ending because Keyboard interruption")

        return min_energy, optimal_parameters
