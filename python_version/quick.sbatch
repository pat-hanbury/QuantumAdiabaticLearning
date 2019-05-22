#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=00:00:10
#SBATCH --job-name=quick-test
#SBATCH --partition=general

/home/hanbury.p/py3-env/env/bin/python3 /home/hanbury.p/feiguin/vmc/main.py