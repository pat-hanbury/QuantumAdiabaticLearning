config = {
    'name': '8LR-Schedualer-test', # name of job
    'num_particles' : 8,
    'num_steps' : 3000, # number of monte carlo steps
    'deltas' : [x/20 for x in range(0,21)],
    'notes' : """
              Testing the new LR schedualing which uses probing
              """,
    'visdom_port' : None,
    'visdom_server': None,
    # 'fixed_params' : ["a", "b"], # fixes parameters to 0
    'noise_scale' : 0.01,
    'Algorithm': 'Algorithm_1',
    'convergence_indicator' : 0.0001,
    'Enumeration' : True,
    'checkpoint' : None,
    'learning_rates' : 0.1,# list of learning rates. If float, same LR will be used for all deltas
    'iterations_list': 50, # number of monte carlo simulations per delta
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