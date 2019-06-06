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
from lib.enumeration_qvmc.utils import setup_save_directories, check_configs, get_four_particle_diamer_W_matrix, generate_new_parameters

from configs import config

import os
import datetime

from pdb import set_trace

if __name__ == '__main__':
    
    global_start = datetime.datetime.now()
    
    check_configs(config)
    setup_save_directories(config)
    print("Run Configurations:")
    pprint(config)
    print("*****"*10)
    print('\n')

    initial_parameters = {
                "a" : np.asarray([0 for i in range(4)]),
                "b" : np.asarray([0 for i in range(4)]),
                "w" : get_four_particle_diamer_W_matrix(config)
                }

    fixed_parameters = dict()
    num_particles = 2
    is_final_hamiltonian = False # set to true at last hamiltonian
    while(not is_final_hamiltonian):
        num_particles = 2*num_particles # number of particles doubles in each hamiltonian
        fixed_parameters.update((key, np.asarray([0 for i in range(num_particles)])) for key in config['fixed_params'])
        print(f"N={num_particles}")
        if num_particles >= config['num_particles']: # should never be greater than
            is_final_hamiltonian = True
            
        # loop through each delta for a given sized hamiltonian
        running_deltas = []
        energies = []
        start_checkpoint = datetime.datetime.now()
        for delta in config['deltas']:
            plotter = Plotter(delta, config['save_dir'], num_particles)
            H = Hamiltonian(num_particles, is_final_hamiltonian, delta=delta)
            
            if delta == config['deltas'][0] and num_particles == 4: # add random noise
                opt = Optimizer(H, config['num_steps'], cfg=config, plotter=plotter,
                                parameters = initial_parameters, lr = config['learning_rate'], 
                                random_noise_scale=config['noise_scale'],
                                fixed_parameters = fixed_parameters)
            else: # no random noise
                opt = Optimizer(H, config['num_steps'], cfg=config, plotter=plotter,
                                parameters = initial_parameters, lr = config['learning_rate'], 
                                fixed_parameters = fixed_parameters)
            energy, optimal_parameters, final_parameters = opt.get_ground_state()
            initial_parameters = optimal_parameters
            energies.append(energy)
            running_deltas.append(delta)
            # print(f"Delta: {delta}")
            # print(f"Variational Energy: {energy}")
            # print("***"*20)

        # generate new initial parameters with the
        # parameters of the previous hamiltonian solution
        initial_parameters = generate_new_parameters(initial_parameters)
        print(initial_parameters)
        time.sleep(10)
        plotter = Plotter(delta, config['save_dir'], num_particles)

        plotter.save_plot(running_deltas, energies, 
                          title=f"Energy(delta) for N={num_particles}",
                          xlabel="Delta", ylabel="Variational Energy",
                          fn=f"{num_particles}_particle_optimization.png")
        
        end_checkpoint = datetime.datetime.now()
        print("*******"*10)
        print(f"Output for N={num_particles} Hamiltonian")
        print("---"*20)
        total_time = ((end_checkpoint - start_checkpoint).total_seconds())/3600
        print(f"Total time = {total_time} hours")
        print("Parameters:")
        pprint(optimal_parameters)
        print("---"*20)
        print("Summary: ")
        for energy, delta in zip(energies, config['deltas']):
            print(f"Delta: {delta:.2f}")
            print(f"Energy: {energy.real:.2E} + {energy.imag:.2E}j")
            print("---"*20)
            print("\n"*5)
    
    # after everything has completed
    global_end = datetime.datetime.now()
    total_time = ((global_start - global_end).total_seconds())/3600
    print(f"Total time: {total_time}")
    
    


