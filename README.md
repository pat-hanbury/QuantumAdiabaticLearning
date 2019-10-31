# Quantum Adiabatic Learning

This repo provides an actively developing implementation of the Quantum Adiabatic Algorithm, a new algorithm for calculating the ground state energies of spin systems, using incrementally solved Restricted Boltzmann Machines.

## Some Background (For the ML People)
In particle physics, elementary particles can have intrinsic angular momentum, which is called a spin. The direction of a spin is binary, and can either be "spin up" or "spin down". A spin system is a geometric collection of spins. For example, a 1-D 8 particle spin system can look like this:

[Image]

Spin systems can be represented as bitstrings. For example, the above spin system would be 11111111.

## The problem
An important quantity for describing spin systems is the ground state energy of the system, which is the lowest possible energy the system can have. Analytically, the ground state energy for any spin system can be solved by constructing the Hamiltonian and determining its eigenvalues and eigenvectors. The Hamiltonian is a matrix embedded with energy information about a quantum system. However, the size of the Hamiltonian grows exponentially with the number of particles, so for larger systems this is computationally infeasible. 

The problem we are trying to solve is to find computationally less expensive ways to determine the ground state energy of spin systems.

## The Solution
Solutions exist to solve the ground state energies for multiparticle spin systems. One promising solution is the use of Restricted Boltzmann Machines. Unlike the Hamiltonian, the size of a RBM modeling a spin system grows linearly with the size of the spin system. It has been shown that optimizing a RBM can lead to finding the ground state energy and associated eigenvector (spin state) of the system. However, RBMs are prone to finding local minimum states, instead of the optimized solution. The Quantum Adiabatic Learning Algorithm seeks to solve this issue by incrementally solving easier problems. We will see below exactly how this works.

The mathematical equation for a Hamiltonian looks like this:
[Hamiltonian Image]

We propose a different Hamiltonian function like this:
[Ham 2]

At δ = 0, this new Hamiltonian is identical to the Hamiltonian of interest. At δ = 1, this Hamiltion is known as the "diamer state" of a spin system. A helpful property of the diamer state is that the parameters of the RBM modeling this state can be solved analytically, without optimization. 

The Quantum Adiabatic Algorithm works by varying δ from 1 to 0 incrementally, solving the problem at each increment by exploiting the parametric similarity between the RBM wave functions. The advantage of this method is that the initial conditions of each incremental optimization problem are so close to the optimized solution that the local minimum solutions can be avoided.

## The algorithms
The Quantum Adiabatic Algorithm takes two forms - Algorithm 1 and Algorithm 2. Algorithm 1 follows the simpler form described above:

#### Quantum Adiabatic Learning (Algorithm 1)
> 1. Generate RBM initial parameters 𝑊0 for H(δ0= 1) analytically
> 2. While(δ >0)
>    - Reduce δ
>    - Optimize parameters W(δ) for H(δ) using VMC with initial
parameters from previous run

Algorithm 2 is an extension of algorithm 1. It involves solving spin systems are smaller sizes using Algorithm 1 to initial parameters for larger systems. For example, when solving a 16 particle system, you would firstly solve a 2 particle system, then use the parameters of this solution as the initial parameters to solve a 4 particle system. You would then use the parameters of a 4 particle system to solve the 8 particle system and so on until you have solved your 16 particle system.

## How to Use this Repo
To do

## Acknowledgements
This research was directed by Professor Adrian Feiguin of Northeastern University, and conceived and guided by Douglas Henry of Northeastern University.

## References
[1] J. Biamonte, P. Wittek, N. Pancotti, P. Rebentrost, N.
Wiebe, and S. Lloyd, Quantum Machine Learning, Nature
(London) 549, 195 (2017).
[2] G. Carleo and M. Troyer, Solving the Quantum ManyBody Problem with Artificial Neural Networks, Science
355, 602 (2017).
