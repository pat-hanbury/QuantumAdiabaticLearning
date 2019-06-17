#!python
#cython: language_level=3

from matplotlib import pyplot as plt
import os

from pprint import pprint

import numpy as np

from lib.qvmc.utils import get_four_particle_diamer_W_matrix, get_initial_w

class Plotter:
    def __init__(self, delta, save_root_dir, num_particles, lr='N/A', display_parameters=None):
        self.N = num_particles
        self.display_parameters = display_parameters # max number of params to display per chart
        self.parameter_history = None
        self.energy_history = []
        self.delta = delta
        self.save_dir = os.path.join(save_root_dir, "plots")
        self.plot_real_time = False
        self.lr = lr
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        

    def update_history(self, energy, w_parameters):
        if len(self.energy_history) == 0:
            self.energy_history = [energy]
        else:
            self.energy_history.append(energy)

        if self.parameter_history is None:
            self.parameter_history = [[param] for param in w_parameters]
        else:
            for i, param in enumerate(w_parameters):
                self.parameter_history[i].append(param)

                
    def show_plot(self):
        if True:
            plt.figure()
            if self.display_parameters is not None:
                for param in self.parameter_history[:self.display_parameters - 1]:
                    plt.plot(param, self.energy_history)
                    plt.plot(param[0], self.energy_history[0], 'go')
                    plt.plot(param[-1], self.energy_history[-1], 'ro')
            else:
                for param in self.parameter_history:
                    plt.plot(param, self.energy_history)
                    plt.plot(param[0], self.energy_history[0], 'go')
                    plt.plot(param[-1], self.energy_history[-1], 'ro')
            plt.xlabel(f"Parameters: W")
            plt.ylabel(f"Variational Energy")
            plt.title(f"Energies for W for delta = {self.delta}")
            
            if True:
                plt.figure()
                for param in self.parameter_history:
                    plt.plot([x.imag for x in param], self.energy_history)
                    for i in range(len(param[0])):
                        plt.plot(param[0][i].imag, self.energy_history[0], 'go')
                        plt.plot(param[-1][i].imag, self.energy_history[-1], 'ro')
                    plt.xlabel(f"Parameters: W")
                    plt.ylabel(f"Variational Energy")
                    plt.title(f"IMAGINARY Energies for W for delta = {self.delta}")
            
        plt.show()
        
    def save_plot(self, xs, ys, title, xlabel, ylabel, fn):
        fig = plt.figure()
        plt.plot(xs, ys)
        plt.plot(xs[0], ys[0], 'go')
        plt.plot(xs[-1], ys[-1], 'ro')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        fig.savefig(os.path.join(self.save_dir, fn))
        plt.close(fig)
        
    def save_parameter_plot(self):
        if True:
            if True: # only print for ws
                fig = plt.figure()
                for param in self.parameter_history:
                    plt.plot([x.imag for x in param], self.energy_history)
                    for i in range(len(param[0])):
                        plt.plot(param[0][i].imag, self.energy_history[0], 'go')
                        plt.plot(param[-1][i].imag, self.energy_history[-1], 'ro')
                    plt.xlabel(f"Parameters: W")
                    plt.ylabel(f"Variational Energy")
                    plt.title(f"Imaginary Parts for W Parameter for delta = {self.delta:.2f}, lr={self.lr}")
                fig.savefig(os.path.join(self.save_dir, f"{self.N}_W_imag_{self.delta:.2f}.png"))
                
                # print real part for all other parameters
                fig = plt.figure()
                for param in self.parameter_history:
                    plt.plot([x.real for x in param], self.energy_history)
                    if True:
                         for i in range(len(param[0])):
                            plt.plot(param[0][i].real, self.energy_history[0], 'go')
                            plt.plot(param[-1][i].real, self.energy_history[-1], 'ro')
                    else:
                        plt.plot(param[0].real, self.energy_history[0], 'go')
                        plt.plot(param[-1].real, self.energy_history[-1], 'ro')
                    plt.xlabel(f"Parameters: W")
                    plt.ylabel(f"Variational Energy")
                    plt.title(f"Real Parts for W Parameter for delta = {self.delta:.2f}, lr={self.lr}")
                fig.savefig(os.path.join(self.save_dir, f"{self.N}_W_real_{self.delta:.2f}.png"))
                plt.close(fig)
            
        self.save_plot(np.arange(len(self.energy_history)), self.energy_history,
                 f"Energy History for {self.delta:.2f}, lr={self.lr}", "Iteration", "Energy", f"{self.N}_EnergyHistory_{self.delta:.2f}.png")
        
        
class CheckpointManager:
    def __init__(self, config):
        self.config = config
        self.checkpoint_dir = os.path.join(config['save_dir'], "training_checkpoints")
        self.countdown = 3 # save every X checkpoints
        
    def should_save(self):
        if self.countdown == 0:
            self.countdown = 3
            return True
        else:
            self.countdown -= 1
            return False
        
    def save_checkpoint(self, w_parameters, iteration):
        if self.should_save():
            path = os.path.join(self.checkpoint_dir, 
                    f"delta{self.delta}_iter{iteration}.npy")
            np.save(path, w_parameters)
        
    def update_delta(self, delta):
        self.delta = delta
        
    def load_checkpoint(self):
        path = self.config["checkpoint"]
        if path is not None:
            return np.load(path)
        else:
            if self.config['Algorithm'] == 'Algorithm_1':
                return get_initial_w(self.config["num_particles"])
            else:
                return get_four_particle_diamer_W_matrix()
        
        
class LogFileWriter:
    def __init__(self, config):
        self.logfile_path = os.path.join(config["save_dir"], 'logfile.txt')
        
    def write(self, obj, precursor=None):
        with open(self.logfile_path, 'a+') as fb:
            pprint("*****"*7, fb)
            if precursor is not None:
                pprint(precursor, fb)
            pprint(obj, fb)
            pprint("*****"*7, fb)