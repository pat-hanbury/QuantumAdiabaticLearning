import numpy as np
import matplotlib as mpl
from pprint import pprint

from matplotlib import pyplot as plt
mpl.use("Agg")
import time

from pprint import pprint
import pickle

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
    
log_file_path = os.path.join(save_dir, "logfile.txt")


checkpoints_dir = os.path.join(cfg["save_dir"], "checkpoints")
   
if not os.path.exists(checkpoints_dir):
    os.makedirs(checkpoints_dir)
    
if cfg["checkpoint"] is not None:
    with open(cfg['checkpoint'], 'rb') as fb:
        initial_parameters = pickle.load(fb)
        starting_delta = cfg["checkpoint"][-10:-7]
    start = int(float(starting_delta)*100)
    cfg["deltas"] = [x/100 for x in range(start, 101, 5)]
else:
    initial_parameters = {
                "a" : np.asarray([0 for i in range(cfg['num_particles'])]),
                "b" : np.asarray([0 for i in range(cfg['num_particles'])]) ,
                "w" : get_initial_w(cfg['num_particles'])
                }
    start = 0
    cfg["deltas"] = [x/100 for x in range(start, 101, 5)]

cfg['fixed_params'] =  {"a" : initial_parameters['a'],
                         "b" : initial_parameters['b']}
with open(log_file_path, 'a+') as log_file:
    pprint("*******"*10, log_file)
    pprint(cfg, log_file)
    pprint("******"*10, log_file)

running_deltas = []
energies = []
start = datetime.datetime.now()
for delta in cfg['deltas']:
    plotter = Plotter(delta, save_dir)
    H = Hamiltonian(cfg['num_particles'], delta=delta)
    if delta == cfg['deltas'][0]: # add random noise
        opt = Optimizer(H, cfg=cfg, plotter=plotter,
                        parameters = initial_parameters, lr = cfg['learning_rate'], random_noise_scale=0.02,
                        fixed_parameters = cfg['fixed_params'])
    else: # no random noise
        opt = Optimizer(H, cfg=cfg, plotter=plotter,
                        parameters = initial_parameters, lr = cfg['learning_rate'], 
                        fixed_parameters = cfg['fixed_params'])
    energy, optimal_parameters, final_parameters = opt.get_ground_state()
    initial_parameters = optimal_parameters
    energies.append(energy)
    running_deltas.append(delta)
    # print(f"Delta: {delta}")
    # print(f"Variational Energy: {energy}")
    # print("***"*20)
        
    with open(os.path.join(checkpoints_dir,f"checkpoint_{delta}.pickle"), 'wb') as f:
        pickle.dump(optimal_parameters, f, pickle.HIGHEST_PROTOCOL)
        
end = datetime.datetime.now()

plotter = Plotter(delta, save_dir)

plotter.save_plot(running_deltas, energies, title="Energy(delta)",
                 xlabel="Delta", ylabel="Variational Energy",
                 fn="FinalOutput.png")

with open(log_file_path, 'a+') as log_file:
    pprint("---"*20, log_file)
    pprint(f"Total time = {((end - start).total_seconds())/3600} hours", log_file)
    if cfg['print_params']:
        pprint("Final Parameters:", log_file)
        pprint(final_parameters, log_file)
        pprint('\n'*2, log_file)
        pprint("Optimal Parameters:", log_file)
        pprint(optimal_parameters, log_file)
    pprint("---"*20, log_file)
    pprint("Final Summary: ", log_file)
    for energy, delta in zip(energies, cfg['deltas']):
        pprint(f"Delta: {delta:.2f}", log_file)
        pprint(f"Energy: {energy.real:.2E} + {energy.imag:.2E}j", log_file)
        pprint("---"*20, log_file)

    

