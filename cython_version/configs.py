cfg = {
    'name' : 'NULL',
    'num_particles' : 8,
    'num_steps' : 10000, # number of monte carlo steps
    'num_monte_carlos_per_delta': 200, # number of monte carlo simulations per delta
    'deltas' : [x/20 for x in range(21)],
    'notes' : """
              Energy Landscape Calculations
              """,
    'print_params' : False,
    'learning_rate' : 0.01,
}