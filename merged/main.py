import numpy as np
import matplotlib as mpl
from pprint import pprint

from matplotlib import pyplot as plt
mpl.use("Agg")
import time

from pprint import pprint

from lib.qvmc.hamiltonian import Hamiltonian
from lib.qvmc.state import State
from lib.qvmc.optimizer import Optimizer
from lib.qvmc.debug import Plotter, LogFileWriter, CheckpointManager
from lib.qvmc.utils import setup_save_directories, check_configs, get_four_particle_diamer_W_matrix, generate_new_parameters

from configs import config

import os
import datetime

from pdb import set_trace

def load_checkpoint(config):
    if config['checkpoint'] is not None:
        with open(cfg['checkpoint'], 'rb') as fb:
            w_parameters = pickle.load(fb)
            starting_delta = cfg["checkpoint"][-10:-7]
        start = int(float(starting_delta)*100)
        config["deltas"] = [x/100 for x in range(start, 101, 5)]
    else:
        if config['Algorithm'] == 'Algorithm_1':
            w_parameters = get_initial_w(config["num_particles"])
        else:
            w_parameters = get_four_particle_diamer_W_matrix()
        start = 0
        config["deltas"] = [x/100 for x in range(start, 101, 5)]
        
    return w_parameters, config


def algorithm1(config):
    initial_ws, config = load_checkpoint(config)
    
    for delta in config['deltas']:
        plotter = plotter(delta, configs['save_dir'])
        H = Hamiltonian(configs["num_particles"], delta=delta)
        opt = Optimizer(H, configs['num_steps'], cfg=configs, 
                        delta, plotter=plotter,
                        parameters = initial_parameters, 
                        lr = configs['learning_rate'])
        energy, optimal_parameters, final_parameters = opt.get_ground_state()
        initial_parameters = optimal_parameters
        plotter.save_plot(running_deltas, energies, title="Energy(delta)",
                 xlabel="Delta", ylabel="Variational Energy",
                 fn="FinalOutput.png")
    

if __name__ == '__main__':
    
    global_start = datetime.datetime.now()
    
    check_configs(config)
    setup_save_directories(config)
    logfile_writter = LogFileWriter(config)
    logfile_writter.write(config)
    
    if config['Algorithm'] == 'Algorithm_1':
        algorithm1(config)
        
    elif config['Algorithm'] == 'Algorithm_2':
        print("NOT Yet implemented")
        algorithm2(config)
        
        
     # after everything has completed
    global_end = datetime.datetime.now()
    total_time = ((global_start - global_end).total_seconds())/3600
    logfile_writter.write(f"Total time: {total_time}")