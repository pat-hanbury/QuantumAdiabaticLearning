from matplotlib import pyplot as plt

class Plotter:
    def __init__(self,delta, display_parameters=None):
        self.display_parameters = display_parameters # max number of params to display per chart
        self.parameter_history = {}
        self.energy_history = []
        self.delta = delta

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
            else:
                for param in self.parameter_history[key]:
                    plt.plot(param, self.energy_history)
            plt.xlabel(f"Parameters: {key}")
            plt.ylabel(f"Variational Energy")
            plt.title(f"Energies for {key} for delta = {self.delta}")
            
            if key == "w":
                plt.figure()
                for param in self.parameter_history[key]:
                    plt.plot([x.imag for x in param], self.energy_history)
                    plt.xlabel(f"Parameters: {key}")
                    plt.ylabel(f"Variational Energy")
                    plt.title(f"IMAGINARY Energies for {key} for delta = {self.delta}")
            
        plt.show()
