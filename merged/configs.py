config = {
    'name': 'HigherLRSFrom0.2', # name of job
    'num_particles' : 16,
    'num_steps' : 3000, # number of monte carlo steps
    'deltas' : [x/20 for x in range(3,21)],
    'notes' : """
              Continued from "HigherLRSFrom0.1" Tuesday @ 11:30am after it only
              had done delta=0.1
              
              Purpose is to increase learning rates for the next few even more
              """,
    'visdom_port' : None,
    'visdom_server': None,
    # 'fixed_params' : ["a", "b"], # fixes parameters to 0
    'noise_scale' : 0.01,
    'Algorithm': 'Algorithm_1',
    'Enumeration' : True,
    'checkpoint' : '/home/hanbury.p/feiguin/vmc/merged/outputs/HigherLRSFrom0.1/2019-06-18-09:25/training_checkpoints/delta0.1_iter27.npy',
    'learning_rates' : [ # 0.0 # 0.05 # 0.10
                        0.2, # 0.15
                        0.2, # 0.20
                        0.15, # 0.25
                        0.15, # 0.30
                        0.1, # 0.35
                        0.1, # 0.40
                        0.1, # 0.45
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
    'iterations_list': [ # 0.0 # 0.05 # 0.10
                        90, # 0.15
                        90, # 0.20
                        90, # 0.25
                        90, # 0.30
                        90, # 0.35
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