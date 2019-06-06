config = {
    'name': 'MergedTest1', # name of job
    'num_particles' : 4,
    'num_steps' : 10000, # number of monte carlo steps
    'num_monte_carlos_per_delta': 400, # number of monte carlo simulations per delta
    'deltas' : [x/20 for x in range(21)],
    'notes' : """
              To test the merged option
              """,
    'fixed_params' : ["a", "b"], # fixes parameters to 0
    'learning_rate' : 0.01,
    'noise_scale' : 0.01
    'Algorithm': 'Algorithm_1',
    'Enumeration' : True,
    'checkpoint' = None
}