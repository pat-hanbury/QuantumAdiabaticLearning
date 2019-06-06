from matplotlib import pyplot as plt
import os

import pprint

import numpy as np

class Plotter:
    def __init__(self, delta, save_root_dir, display_parameters=None):
        self.display_parameters = display_parameters # max number of params to display per chart
        self.parameter_history = {}
        self.energy_history = []
        self.delta = delta
        self.save_dir = os.path.join(save_root_dir, "plots")
        self.plot_real_time = False
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        

    def update_history(self, energy, parameters_dict):
        if len(self.energy_history) == 0:
            self.energy_history = [energy]
        else:
            self.energy_history.append(energy)

        for key, parameters in parameters_dict.items():
            if self.parameter_history.get(key, None) is None:
                self.parameter_history[key] = [[param] for param in parameters]
            else:
                for i, param in enumerate(parameters):
                    self.parameter_history[key][i].append(param)

    def show_plot(self):
        for key, parameters in self.parameter_history.items():
            plt.figure()
            if self.display_parameters is not None:
                for param in self.parameter_history[key][:self.display_parameters - 1]:
                    plt.plot(param, self.energy_history)
                    plt.plot(param[0], self.energy_history[0], 'go')
                    plt.plot(param[-1], self.energy_history[-1], 'ro')
            else:
                for param in self.parameter_history[key]:
                    plt.plot(param, self.energy_history)
                    plt.plot(param[0], self.energy_history[0], 'go')
                    plt.plot(param[-1], self.energy_history[-1], 'ro')
            plt.xlabel(f"Parameters: {key}")
            plt.ylabel(f"Variational Energy")
            plt.title(f"Energies for {key} for delta = {self.delta}")
            
            if key == "w":
                plt.figure()
                for param in self.parameter_history[key]:
                    plt.plot([x.imag for x in param], self.energy_history)
                    for i in range(len(param[0])):
                        plt.plot(param[0][i].imag, self.energy_history[0], 'go')
                        plt.plot(param[-1][i].imag, self.energy_history[-1], 'ro')
                    plt.xlabel(f"Parameters: {key}")
                    plt.ylabel(f"Variational Energy")
                    plt.title(f"IMAGINARY Energies for {key} for delta = {self.delta}")
            
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
        for key, parameters in self.parameter_history.items():
            if key == 'w': # only print for ws
                fig = plt.figure()
                for param in self.parameter_history[key]:
                    plt.plot([x.imag for x in param], self.energy_history)
                    for i in range(len(param[0])):
                        plt.plot(param[0][i].imag, self.energy_history[0], 'go')
                        plt.plot(param[-1][i].imag, self.energy_history[-1], 'ro')
                    plt.xlabel(f"Parameters: {key}")
                    plt.ylabel(f"Variational Energy")
                    plt.title(f"Imaginary Parts for {key} Parameter for delta = {self.delta:.2f}")
                fig.savefig(os.path.join(self.save_dir, f"{key}_imag_{self.delta:.2f}.png"))
                
                # print real part for all other parameters
                fig = plt.figure()
                for param in self.parameter_history[key]:
                    plt.plot([x.real for x in param], self.energy_history)
                    if key == 'w':
                         for i in range(len(param[0])):
                            plt.plot(param[0][i].real, self.energy_history[0], 'go')
                            plt.plot(param[-1][i].real, self.energy_history[-1], 'ro')
                    else:
                        plt.plot(param[0].real, self.energy_history[0], 'go')
                        plt.plot(param[-1].real, self.energy_history[-1], 'ro')
                    plt.xlabel(f"Parameters: {key}")
                    plt.ylabel(f"Variational Energy")
                    plt.title(f"Real Parts for {key} Parameter for delta = {self.delta:.2f}")
                fig.savefig(os.path.join(self.save_dir, f"{key}_real_{self.delta:.2f}.png"))
                plt.close(fig)
            
        self.save_plot(np.arange(len(self.energy_history)), self.energy_history,
                 f"Energy History for {self.delta:.2f}", "Energy", "Iteration", f"EnergyHistory_{self.delta:.2f}.png")
        
class LogFileWriter:
    def __init__(self, config):
        self.logfile_path = os.path.join(config["save_dir"], 'logfile.txt')
        
    def write(self, obj):
        with open(self.logfile_path, 'a+') as fb:
            pprint(obj, fb)