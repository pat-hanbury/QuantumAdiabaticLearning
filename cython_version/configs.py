cfg = {
    'name' : '16ParticleLongerStudy',
    'num_particles' : 4,
    'num_steps' : 20000, # number of monte carlo steps
    'num_monte_carlos_per_delta': 100, # number of monte carlo simulations per delta
    'notes' : """
              Fixed the Q of X function.
              """,
    'print_params' : False,
    'learning_rate' : 0.1,
    # 'LR_list' : [5]
    'checkpoint' : None
}