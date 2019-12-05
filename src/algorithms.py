from lib.qvmc.utils import get_initial_w, get_four_particle_diamer_W_matrix, load_checkpoint, generate_new_parameters
from lib.qvmc.debug import Plotter, CheckpointManager
from lib.qvmc.hamiltonian import Hamiltonian
from lib.qvmc.optimizer import Optimizer
from lib.qvmc.visdom_manager import VisdomManager

import datetime

def run_algorithm(config):
    # debugging so we can attach SLURM output to logfile
    print(config)
    
    if config['Algorithm'] == 'Algorithm_1':
        algorithm1(config)

    elif config['Algorithm'] == 'Algorithm_2':
        algorithm2(config)

def algorithm1(config):
    checkpoint_manager = CheckpointManager(config)
    initial_ws = checkpoint_manager.load_checkpoint()
    deltas = config['deltas']
    learning_rates = config["learning_rates"]
    iterations_list = config['iterations_list']
    energies = []
    
    if config["visdom_port"] is not None:
        visdom_manager = VisdomManager(port=config["visdom_port"], server=config["visdom_server"])
    else:
        visdom_manager = None
  
    for i, (delta, lr, iterations) in enumerate(zip(deltas, learning_rates, iterations_list)):
        checkpoint_manager.update_delta(delta)
        if visdom_manager is not None:
            visdom_manager.new_window(f"Energy History delta={delta}")
        plotter = Plotter(delta, config['save_dir'],
                          config["num_particles"], lr=lr)
        H = Hamiltonian(config, is_ring=True, delta=delta)
        opt = Optimizer(H, config=config, 
                        delta=delta, lr=lr, 
                        iterations=iterations,
                        plotter=plotter,
                        checkpoint_manager = checkpoint_manager,
                        visdom_manager=visdom_manager,
                        w_parameters = initial_ws)
        energy, optimal_parameters, final_parameters = opt.get_ground_state()
        energies.append(energy)
        initial_ws = optimal_parameters
        plotter.save_plot(deltas[:i+1], energies, title="Energy(delta)",
                 xlabel="Delta", ylabel="Variational Energy",
                 fn="FinalOutput.png")
        
        
def algorithm2(config):
    checkpoint_manager = CheckpointManager(config)
    initial_ws = checkpoint_manager.load_checkpoint()
    deltas = config['deltas']
    learning_rates = config["learning_rates"]
    iterations_list = config['iterations_list']
    
    if config["visdom_port"] is not None:
        visdom_manager = VisdomManager(port=config["visdom_port"], server=config["visdom_server"])
    else:
        visdom_manager = None
    
    num_particles = len(initial_ws) # number of particle for start
    is_ring = False
    
    while(not is_ring):
        is_ring = (num_particles >= config['num_particles']) # T or F
        use_noise = (num_particles == 4)
        energies = []
        
        for i, (delta, lr, iterations) in enumerate(zip(deltas, learning_rates, iterations_list)):
            checkpoint_manager.update_delta(delta)
            if visdom_manager is not None:
                visdom_manager.new_window(f"Energy History delta={delta}")
            plotter = Plotter(delta, config['save_dir'], 
                              num_particles, lr=lr)
            H = Hamiltonian(config, is_ring=is_ring, delta=delta, num_particles=num_particles)
            # always adds noise for delta=0 for all N
            opt = Optimizer(H, config=config, 
                            delta=delta, lr=lr, 
                            iterations=iterations,
                            plotter=plotter,
                            checkpoint_manager = checkpoint_manager,
                            visdom_manager=visdom_manager,
                            w_parameters = initial_ws, 
                            use_noise=use_noise)
            
            energy, optimal_parameters, final_parameters = opt.get_ground_state()
            initial_ws = optimal_parameters
            energies.append(energy)
            plotter.save_plot(deltas[:i+1], 
                energies, title="Energy(delta)",
                xlabel="Delta", ylabel="Variational Energy",
                fn=f"Optimization_{num_particles}.png")
        
        num_particles*=2
        initial_ws = generate_new_parameters(initial_ws)
        
    