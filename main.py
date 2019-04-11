import numpy as np
from matplotlib import pyplot as plt

import time

from lib.qvmc.hamiltonian import Hamiltonian
from lib.qvmc.state import State
from lib.qvmc.optimizer import Optimizer
from lib.qvmc.debug import Plotter
from lib.qvmc.utils import get_initial_w

# configs
num_particles = 8
num_parameters = 5
num_steps = 20000
delta = 1

initial_parameters = {
            "a" : np.asarray([0 for i in range(num_particles)]),
            "b" : np.asarray([0 for i in range(num_particles)]) ,
            "w" : get_initial_w(num_particles)
            }

fixed_params =  {"a" : initial_parameters['a'],
                 "b" : initial_parameters['b']}
# fixed_params = None

deltas = [0.95-(x/20) for x in range(20)]
running_deltas = []
energies = []
for delta in deltas:
    plotter = None
    H = Hamiltonian(num_particles, delta=delta)
    if delta == deltas[0]: # add random noise
        opt = Optimizer(H, num_steps, plotter=plotter, num_parameters=5,
                    parameters = initial_parameters, lr = 0.02, random_noise_scale=0.02,
                   fixed_parameters = fixed_params)
    else: # no random noise
        opt = Optimizer(H, num_steps, plotter=plotter, num_parameters=5,
                        parameters = initial_parameters, lr = 0.02, fixed_parameters = fixed_params)
    energy, initial_parameters = opt.get_ground_state()
    energies.append(energy)
    running_deltas.append(delta)
    print(f"Delta: {delta}")
    print(f"Variational Energy: {energy}")
    print("***"*20)
plt.plot(running_deltas, energies)
plt.title("Energy(delta)")
plt.xlabel("Delta")
plt.ylabel("Variational Energy")
plt.show()
# time.sleep(4)

print("*******"*10)
print("Final Summary: ")
for energy, delta in zip(energies, deltas):
    print(f"Delta: {delta}")
    print(f"Energy: {energy}")
    print("---"*20)
