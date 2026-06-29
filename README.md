# Cells-in-Microfluidic-devices-simulations-in-CC3D
Programs developed during my scholarship in ICMAB:

## Short explanation of each simulation:

### 1. Advection_Chem

This simulation tries to implement advection to a diffusive chemical field in CC3D. The program uses the main diffusion solver that CC3D has and add in the python script an aproach of a flux in the chemical field in the x direction. It can be extended to 3 dimensions and other directions following a similar structure.

### 2. CellInLiquid

The simulation uses three types of cells to simulate cell behaivour in a liquid with flux. The small type of cell have the objective to work as small bubbles of liquid that is being pushed to the right. Then we have a freezed cell that works as a wall to build the different constrictions of the simulation. And finally the usual cells that grow in the liquid while getting pushed by the liquid.

### 3. CellsInMicrofluidic

This code try to combine the two previous simulation to get an understanding of the cell growth in a Porous Microfluidic Device. A nutrient that limit the cell growth is present that difusses and move with a flux. To avoid using a lot of computational resources the liquid cells of the CellInLiquid simulation where avoided adding insted a force to the cell proportional to the velocity of the flux.

### 4. CellInPorusMicrofluidic

Builds a porus media using a probability distrubiution where cells grow and became more complex thanks to a nutrient present that difuses. Complexity is implemented as a new parameter of each cells that changes while uptaking the nutrient from the media, the cell decides randomly if it grows bigger or it makes the complexity higher.

### 5. CellInPorusMedia3D

Same as *4* but in 3D. There is also a comented block in the steppables that adds a new secretor from the cell that degrades the walls, core idea at simulation *7*.


### 6. ProvesCanviCells

3D simulation that implements a cell eating a wall.

### 7. WallDegradetion

2D simulation of a wall and existing cells that segragate a chemical that degradetes the wall little by little. This is also implemented, but comented in the code, in the simulation *5*.


### 8. WetableGrowth

3D simulation that simulates a group of cells growing in a desired surface. Changing the contact energy between cells and the wall you can see different behaivours.

### 9. ColonyGrowSimulation

Implemented simulation of colony grow based on the work of Kannan, H., Sun, H., Warren, M. et al. (citation below). This simulation ables to study further constraints like geometry effects (circle agar implemented) or different affinities with the wall (contact energies).

Article:
Kannan, H., Sun, H., Warren, M. et al. Spatiotemporal development of expanding bacterial colonies driven by emergent mechanical constraints and nutrient gradients. Nat Commun 16, 4878 (2025). https://doi.org/10.1038/s41467-025-60004-z

### 10. RealisticCellsGrow

Extention of *9* to cells. Here you can change and work with all different parameters from the affinity of cells to the wall, to their growth, the quantity of nutrients etc.

### 11. TCellsActivation2

A 2D simulation that tries an aproach on T-Cells activation. Using a Boltzman-like probability the T-Cells can activate in contact with the wall, higher the contact on the wall higher the probability of activation. When activated the cells change in type (for visual porpouses) and shape and starts to grow and duplicate. When duplicated the T-cells have a probability to become exausted and stop to proliferate, this probability depend on the generation of the cell and can have different shapes to study different behaivours.


### 12. TCellsActivation3D

Extention of *11* to 3D. In addition, there is different geometries of the wall and starting position of cells like dynabeads or random height start from cells for exemple. Also reactivation is implemented as an option if wanted and the sedimentation of cells.
