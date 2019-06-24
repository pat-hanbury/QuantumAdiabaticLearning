config = {
    'name':'200-iters-Continued-0.5', # name of job
    'num_particles' : 16,
    'num_steps' : 3000, # number of monte carlo steps
    'deltas' : [x/20 for x in range(10,21)],
    'notes' : """
              Continued from "300-iters-1.0....
              (which actually used 400 iters).
              
              Appeared linear for 400 iters, suggesting
              we need many more but that it might still converge
              """,
    'visdom_port' : None,
    'visdom_server': None,
    # 'fixed_params' : ["a", "b"], # fixes parameters to 0
    'noise_scale' : 0.01,
    'Algorithm': 'Algorithm_1',
    'convergence_indicator' : 0.0,
    'Enumeration' : True,
    'checkpoint' : "/home/hanbury.p/feiguin/vmc/merged/outputs/200-iters-conitinued-0.4/2019-06-22-15:02/training_checkpoints/delta0.5_iter60.npy",
    'learning_rates' : 0.1,# list of learning rates. If float, same LR will be used for all deltas
    'iterations_list': 200,  # number of monte carlo simulations per delta
}

""" # Learning Rate List
                        [# 0.0 # 0.05
                        0.1, # 0.10
                        0.1, # 0.15
                        0.1, # 0.20
                        0.1, # 0.25
                        0.05, # 0.30
                        0.05, # 0.35
                        0.05, # 0.40
                        0.05, # 0.45
                        0.05, # 0.50
                        0.05, # 0.55
                        0.05, # 0.60
                        0.03, # 0.65
                        0.03, # 0.70
                        0.03, # 0.75
                        0.03, # 0.80
                        0.01, # 0.85
                        0.01, # 0.90
                        0.01, # 0.95
                        0.01, # 1.00 
                       ],# list of learning rates
"""