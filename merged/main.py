import numpy as np
import matplotlib as mpl
from pprint import pprint

from matplotlib import pyplot as plt
mpl.use("Agg")
import time

from pprint import pprint

from lib.qvmc.hamiltonian import Hamiltonian
from lib.qvmc.state import State
from lib.qvmc.optimizer import Optimizer
from lib.qvmc.debug import Plotter, LogFileWriter, CheckpointManager
from lib.qvmc.utils import setup_save_directories, check_configs, generate_new_parameters, get_initial_w

from algorithms import run_algorithm

import line_profiler

from configs import config

import os
import datetime

from pdb import set_trace
    

if __name__ == '__main__':
    
    global_start = datetime.datetime.now()
    config = check_configs(config)
    config = setup_save_directories(config)
    logfile_writter = LogFileWriter(config)
    logfile_writter.write(config, "Configs:")
    
    run_algorithm(config)
        
        
     # after everything has completed
    global_end = datetime.datetime.now()
    total_time = ((global_start - global_end).total_seconds())/3600
    logfile_writter.write("Total time: {total_time}")