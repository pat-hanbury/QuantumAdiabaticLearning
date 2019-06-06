#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=1:00:10
#SBATCH --job-name=enumerationAlgo2
#SBATCH --partition=general

/home/hanbury.p/env/bin/python3 /home/hanbury.p/feiguin/vmc/dynamic_adiabatic/enumeration_setup.py build_ext --inplace && /home/hanbury.p/env/bin/python3 /home/hanbury.p/feiguin/vmc/dynamic_adiabatic/enumeration_run.py