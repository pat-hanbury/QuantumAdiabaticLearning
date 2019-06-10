config = {
    'name': 'Algo2-EnumTest', # name of job
    'num_particles' : 8,
    'num_steps' : 3000, # number of monte carlo steps
    'num_monte_carlos_per_delta': 300, # number of monte carlo simulations per delta
    'deltas' : [x/20 for x in range(21)],
    'notes' : """
              To test the merged option
              """,
    'fixed_params' : ["a", "b"], # fixes parameters to 0
    'learning_rate' : 0.01,
    'noise_scale' : 0.03,
    'Algorithm': 'Algorithm_2',
    'Enumeration' : True,
    'checkpoint' : None,
}