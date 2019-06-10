from lib.qvmc.utils import get_initial_w, get_four_particle_diamer_W_matrix, load_checkpoint, generate_new_parameters

from lib.qvmc.debug import Plotter
from lib.qvmc.hamiltonian import Hamiltonian
from lib.qvmc.optimizer import Optimizer

import datetime

def run_algorithm(config):
    if config['Algorithm'] == 'Algorithm_1':
        algorithm1(config)

    elif config['Algorithm'] == 'Algorithm_2':
        algorithm2(config)

def algorithm1(config):
    initial_ws, config = load_checkpoint(config)
    deltas = config['deltas']
    energies = []
    
    for i, delta in enumerate(deltas):
        plotter = Plotter(delta, config['save_dir'])
        H = Hamiltonian(config, is_ring=True, delta=delta)
        opt = Optimizer(H, config=config, 
                        delta=delta, plotter=plotter,
                        w_parameters = initial_ws)
        energy, optimal_parameters, final_parameters = profile(opt.get_ground_state())
        energies.append(energy)
        initial_ws = optimal_parameters
        plotter.save_plot(deltas[:i+1], energies, title="Energy(delta)",
                 xlabel="Delta", ylabel="Variational Energy",
                 fn="FinalOutput.png")
        
        
def algorithm2(config):
    initial_ws, config = load_checkpoint(config)
    deltas = config['deltas']
    num_particles = len(initial_ws) # number of particle for start
    is_ring = False
    
    while(not is_ring):
        print(num_particles)
        print(config['num_particles'])
        is_ring = (num_particles >= config['num_particles']) # T or F
        use_noise = (num_particles == 4)
        energies = []
        print(f"use noise: {use_noise}")
        
        for i, delta in enumerate(deltas):
            plotter = Plotter(delta, config['save_dir'], num_particles)
            H = Hamiltonian(config, is_ring=is_ring, delta=delta, num_particles=num_particles)
            # always adds noise for delta=0 for all N
            opt = Optimizer(H, config=config, 
                        delta=delta, plotter=plotter,
                        w_parameters = initial_ws, use_noise=use_noise)
            energy, optimal_parameters, final_parameters = opt.get_ground_state()
            initial_ws = optimal_parameters
            energies.append(energy)
            plotter.save_plot(deltas[:i+1], 
                energies, title="Energy(delta)",
                xlabel="Delta", ylabel="Variational Energy",
                fn=f"Optimization_{num_particles}.png")
        
        num_particles*=2
        initial_ws = generate_new_parameters(initial_ws)
        
    