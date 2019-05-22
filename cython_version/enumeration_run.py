import numpy as np
import matplotlib as mpl
from pprint import pprint

from matplotlib import pyplot as plt
mpl.use("Agg")
import time

from pprint import pprint

from lib.enumeration_qvmc.hamiltonian import Hamiltonian
from lib.enumeration_qvmc.state import State
from lib.enumeration_qvmc.optimizer import Optimizer
from lib.enumeration_qvmc.debug import Plotter
from lib.enumeration_qvmc.utils import get_initial_w

from configs import cfg

import os
import datetime

from pdb import set_trace

now = datetime.datetime.now()

# configs

cwd = os.getcwd()

save_dir = os.path.join(cwd, "outputs", cfg['name'], now.strftime("%Y-%m-%d-%H:%M"))

cfg['save_dir'] = save_dir

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    

initial_parameters = {
            "a" : np.asarray([0 for i in range(cfg['num_particles'])]),
            "b" : np.asarray([0 for i in range(cfg['num_particles'])]) ,
            "w" : get_initial_w(cfg['num_particles'])
            }

cfg['fixed_params'] =  {"a" : initial_parameters['a'],
                         "b" : initial_parameters['b']}

running_deltas = []
energies = []
start = datetime.datetime.now()
# set_trace()
for delta in cfg['deltas']:
    plotter = Plotter(delta, save_dir)
    H = Hamiltonian(cfg['num_particles'], delta=delta)
    if delta == cfg['deltas'][0]: # add random noise
        opt = Optimizer(H, cfg=cfg, plotter=plotter,
                        parameters = initial_parameters, lr = 0.02, random_noise_scale=0.02,
                        fixed_parameters = cfg['fixed_params'])
    else: # no random noise
        opt = Optimizer(H, cfg=cfg, plotter=plotter,
                        parameters = initial_parameters, lr = 0.02, 
                        fixed_parameters = cfg['fixed_params'])
    energy, optimal_parameters, final_parameters = opt.get_ground_state()
    initial_parameters = optimal_parameters
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
pprint(cfg)
print("---"*20)
print(f"Total time = {((end - start).total_seconds())/3600} hours")
if cfg['print_params']:
    print("Final Parameters:")
    pprint(final_parameters)
    print('\n'*2)
    print("Optimal Parameters:")
    pprint(optimal_parameters)
print("---"*20)
print("Final Summary: ")
for energy, delta in zip(energies, cfg['deltas']):
    print(f"Delta: {delta:.2f}")
    print(f"Energy: {energy.real:.2E} + {energy.imag:.2E}j")
    print("---"*20)

    

