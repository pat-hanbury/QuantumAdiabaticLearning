import numpy as np


def get_initial_w(num_particles):
    w = np.zeros((num_particles, num_particles), dtype=np.complex_)
    var = 3.14159j / 4
    for i in range(num_particles):
        for j in range(num_particles):
            if (i%2 == 0) and ((i == j) or (j == i + 1)):
                w[i][j] = var
    return w
