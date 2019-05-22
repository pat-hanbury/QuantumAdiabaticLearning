#!python
#cython: language_level=3

import os
import datetime

import numpy as np

from pdb import set_trace


def get_initial_w(num_particles):
    w = np.zeros((num_particles, num_particles), dtype=np.complex_)
    var = 3.14159j / 4
    for i in range(num_particles):
        for j in range(num_particles):
            if (i%2 == 0) and ((i == j) or (j == i + 1)):
                w[i][j] = var
    return w

def get_four_particle_diamer_W_matrix(config):
    """
    Gets W matrix for two particle diamer state.
    Can be 1 of three matrixes, specified in the
    configs.
    1 : W00 = W01 = i*pi/4 and W10=W11 = 0 (normal)
    2 : W00 = W01 = W10=W11 = i*pi/4
    3 : W00 = W01 = i*pi/4 and W10 = W11 = -1*i*pi/4
    """
    var = 3.14159j / 4

    if config['initial_diamer_state'] == 'option_1':
        return np.asarray([[var, var, 0, 0],
                           [0, 0, 0, 0],
                          [0, 0, var, var],
                          [0, 0, 0, 0]], dtype=np.complex_)
    elif config['initial_diamer_state'] == 'option_2':
        return np.asarray([[var, var, 0, 0],
                           [var, var, 0, 0],
                          [0, 0, var, var],
                          [0, 0,var, var,]], dtype=np.complex_)
    elif config['initial_diamer_state'] == 'option_3':
        return np.asarray([[var, var, 0, 0],
                           [var, var, 0, 0],
                          [0, 0, -1*var, -1*var],
                          [0, 0,-1*var, -1*var,]], dtype=np.complex_)
    else:
        error = 'initial_diamer state not a correct option'
        raise ValueError(error)
        
def setup_save_directories(config):
    now = datetime.datetime.now()

    # configs

    cwd = os.getcwd()

    save_dir = os.path.join(cwd, "outputs", config['name'] + '_' + now.strftime("%Y-%m-%d-%H:%M"))

    config['save_dir'] = save_dir

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
def check_configs(config):
    acceptable_options = ['option_1', 'option_2', 'option_3']
    error = 'initial_diamer state not a correct option'
    assert config['initial_diamer_state'] in acceptable_options, error
    
    def is_power_of_two(num):
        return ((num & (num - 1)) == 0) and num > 0
    
    error = 'Number of particles must be a power of two'
    assert(is_power_of_two(config['num_particles'])), error
    
def generate_new_parameters(previous_parameters):
    previous_parameters['w']
    m, n = previous_parameters['w'].shape
    assert m == n, 'Should be using W matrices for this function'
    w = np.zeros((2*m,2*n), dtype=np.complex_)
    w[:m, :n] = previous_parameters['w'].copy()
    w[m:, n:] = previous_parameters['w'].copy()
    
    return  {"a" : np.asarray([0 for i in range(2*m)]),
             "b" : np.asarray([0 for i in range(2*m)]),
             "w" : w }
