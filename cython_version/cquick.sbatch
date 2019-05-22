#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=00:00:10
#SBATCH --job-name=quick-test
#SBATCH --partition=general

/home/hanbury.p/env/bin/python3 /home/hanbury.p/feiguin/vmc/cython_version/setup.py build_ext --inplace && /home/hanbury.p/env/bin/python3 /home/hanbury.p/feiguin/vmc/cython_version/main.py