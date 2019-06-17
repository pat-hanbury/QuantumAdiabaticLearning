config = {
    'name': 'ContinuedFrom0.1-lowerLR', # name of job
    'num_particles' : 16,
    'num_steps' : 3000, # number of monte carlo steps
    'deltas' : [x/20 for x in range(2,21)],
    'notes' : """
              To figure out optimal LR and Iterations so that we can do 16 Particle enumeration
              entirely
              """,
    'visdom_port' : None,
    'visdom_server': None,
    # 'fixed_params' : ["a", "b"], # fixes parameters to 0
    'noise_scale' : 0.01,
    'Algorithm': 'Algorithm_1',
    'Enumeration' : True,
    'checkpoint' : '/home/hanbury.p/feiguin/vmc/merged/outputs/16EnumContinued/2019-06-17-13:04/training_checkpoints/delta0.1_iter57.npy',
    'learning_rates' : [ # 0.0 # 0.05
                        0.05, # 0.10
                        0.05, # 0.15
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
                       ],# list of learning rates. If float, same LR will be used for all deltas
    'iterations_list': [ # 0.0 # 0.05
                        30, # 0.10
                        75, # 0.15
                        75, # 0.20
                        75, # 0.25
                        75, # 0.30
                        75, # 0.35
                        90, # 0.40
                        90, # 0.45
                        90, # 0.50
                        90, # 0.55
                        120, # 0.60
                        120,  # 0.65
                        120, # 0.70
                        120, # 0.75
                        120, # 0.80
                        150, # 0.85
                        150, # 0.90
                        150, # 0.95
                        150  # 1.00
                       ], # number of monte carlo simulations per delta
}