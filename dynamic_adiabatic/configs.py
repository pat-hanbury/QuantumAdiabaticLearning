config = {
    'name': '8FixedConjugate', # name of job
    'num_particles' : 8,
    'num_steps' : 10000, # number of monte carlo steps
    'num_monte_carlos_per_delta': 200, # number of monte carlo simulations per delta
    'deltas' : [x/20 for x in range(21)],
    'notes' : """
              This is to test the fixed
              conjugate problem when 
              taking derivatives
              """,
    'initial_diamer_state' : 'option_1', # number of initial diamer state we want to use. See code for 3 options
     'fixed_params' : ["a", "b"], # fixes parameters to 0
    'learning_rate' : 0.01,
    'noise_scale' : 0.01
}