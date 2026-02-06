# Cells-in-Microfluidic-devices-simulations-in-CC3D
Programs developed during my scholarship in ICMAB:

## Short explanation of each simulation:

### 1. Advection_Chem

This simulation tries to implement advection to a diffusive chemical field in CC3D. The program uses the main diffusion solver that CC3D has and add in the python script an aproach of a flux in the cells lattice in the x direction. It can be extended to 3 dimensions and other directions following a similar structure.

### 2. CellInLiquid

The simulation uses three types of cells to simulate cell behaivour in a liquid with flux. The small type of cell have the objective to work as small bubbles of liquid that is being pushed to the right. Then we have a freezed cell that works as a wall to build the different constrictions of the simulation. And finally the usual cells that grow in the liquid while getting pushed by the liquid.
