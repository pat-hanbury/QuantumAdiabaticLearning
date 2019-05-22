#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=23:00:10
#SBATCH --job-name=cython_4particle_test
#SBATCH --partition=general

/home/hanbury.p/env/bin/python3 /home/hanbury.p/feiguin/vmc/cython_version/setup.py build_ext --inplace && /home/hanbury.p/env/bin/python3 /home/hanbury.p/feiguin/vmc/cython_version/main.py