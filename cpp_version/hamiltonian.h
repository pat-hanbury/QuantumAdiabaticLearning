#ifndef HAMILTONIAN_H
#define

class Hamiltonian
{
 private:
   int num;
 public:
   // constructor
   Hamiltonian(int num_particles, float delta);

   float calculate_local_energy();
};

#endif
