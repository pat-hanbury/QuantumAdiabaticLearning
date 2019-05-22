#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=23:00:10
#SBATCH --job-name=dynamicAdiabaticMain
#SBATCH --partition=general

/home/hanbury.p/env/bin/python3 /home/hanbury.p/feiguin/vmc/dynamic_adiabatic/setup.py build_ext --inplace && /home/hanbury.p/env/bin/python3 /home/hanbury.p/feiguin/vmc/dynamic_adiabatic/main.py