#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=1:00:01
#SBATCH --job-name=8_particle_ground_state_test
#SBATCH --partition=general

/home/hanbury.p/env/bin/python3 /home/hanbury.p/feiguin/vmc/main.py