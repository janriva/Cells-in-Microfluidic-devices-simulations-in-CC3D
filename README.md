# Cells-in-Microfluidic-devices-simulations-in-CC3D
Programs developed during my scholarship in ICMAB:

## Short explanation of each simulation:

### 1. Advection_Chem

This simulation tries to implement advection to a diffusive chemical field in CC3D. The program uses the main diffusion solver that CC3D has and add in the python script an aproach of a flux in the cells lattice in the x direction. It can be extended to 3 dimensions and other directions following a similar structure.

### 2. CellInLiquid

The simulation uses three types of cells to simulate cell behaivour in a liquid with flux. The small type of cell have the objective to work as small bubbles of liquid that is being pushed to the right. Then we have a freezed cell that works as a wall to build the different constrictions of the simulation. And finally the usual cells that grow in the liquid while getting pushed by the liquid.

### 3. CellsInMicrofluidic

This code try to combine the two previous simulation to get an understanding of the cell growth in a Porous Microfluidic Device. A nutrient that limit the cell growth is present that difusses and move with a flux. To avoid using a lot of computational resources the liquid cells of the CellInLiquid simulation where avoided adding insted a force to the cell proportional to the velocity of the flux.

### 4. CellInPorusMicrofluidic

Builds a porus media using a probability distrubiution where cells grow and became more complex thanks to a nutrient present that difuses. Complexity is implemented as a new parameter of each cells that changes while uptaking the nutrient from the media, the cell decides randomly if it grows bigger or it makes the complexity higher.


There is a comented block that adds a new secretor from the cell that degrades the walls
