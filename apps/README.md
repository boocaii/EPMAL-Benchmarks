------------------------------------------------
# App 01: Kripke
------------------------------------------------
## src
https://github.com/LLNL/Kripke

## modules used
module load python/3.6.1
module load cmake/3.6.1
module load gcc/7.3.0
module load openmpi/3.1.0/gcc/7.3.0



------------------------------------------------
# App 02: new_ij with hypre
------------------------------------------------
## src
https://github.com/LLNL/hypre

## modules used
  
## compiling
cd src
./configure
make
