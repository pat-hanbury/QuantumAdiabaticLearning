import numpy as np
import matplotlib as mpl

from matplotlib import pyplot as plt
mpl.use("Agg")
import time

from lib.qvmc.hamiltonian import Hamiltonian
from lib.qvmc.state import State
from lib.qvmc.optimizer import Optimizer
from lib.qvmc.debug import Plotter
from lib.qvmc.utils import get_initial_w

from pprint import pprint

import os
import datetime

purpose = """
Run just for delta = 0.99
"""

now = datetime.datetime.now()

print(now)

# configs
num_particles = 8
num_steps = 5000
delta = 1

save_dir = os.path.join("/home/hanbury.p/feiguin/vmc/outputs/", now.strftime("%Y-%m-%d-%H:%M"))

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    

initial_parameters = {
            "a" : np.asarray([0 for i in range(num_particles)]),
            "b" : np.asarray([0 for i in range(num_particles)]) ,
            "w" : get_initial_w(num_particles)
            }

fixed_params =  {"a" : initial_parameters['a'],
                 "b" : initial_parameters['b']}
# fixed_params = None

# deltas = [0.95-(x/20) for x in range(20)] + [0.975-(x/20) for x in range(6)]
deltas = [0.99]
deltas.sort(reverse=True)
running_deltas = []
energies = []
start = datetime.datetime.now()
for delta in deltas:
    plotter = Plotter(delta, save_dir)
    H = Hamiltonian(num_particles, delta=delta)
    if delta == deltas[0]: # add random noise
        opt = Optimizer(H, num_steps, plotter=plotter, num_parameters=5,
                    parameters = initial_parameters, lr = 0.02, random_noise_scale=0.02,
                   fixed_parameters = fixed_params)
    else: # no random noise
        opt = Optimizer(H, num_steps, plotter=plotter, num_parameters=5,
                        parameters = initial_parameters, lr = 0.02, fixed_parameters = fixed_params)
    energy, opt_parameters, final_parameters = opt.get_ground_state()
    initial_parameters = final_parameters
    energies.append(energy)
    running_deltas.append(delta)
    # print(f"Delta: {delta}")
    # print(f"Variational Energy: {energy}")
    # print("***"*20)
end = datetime.datetime.now()

plotter = Plotter(delta, save_dir)

plotter.save_plot(running_deltas, energies, title="Energy(delta)",
                 xlabel="Delta", ylabel="Variational Energy",
                 fn="FinalOutput.png")

print("*******"*10)
print(purpose)
print(f"Saved in {save_dir}")
print("---"*20)
print(f"Total time = {((end - start).total_seconds())/3600} hours")
print("---"*20)
print("Final Parameters:")
pprint(final_parameters)
print("---"*20)
print("Final Summary: ")
for energy, delta in zip(energies, deltas):
    print(f"Delta: {delta:.2f}")
    print(f"Energy: {energy.real:.2E} + {energy.imag:.2E}j")
    print("---"*20)

    

