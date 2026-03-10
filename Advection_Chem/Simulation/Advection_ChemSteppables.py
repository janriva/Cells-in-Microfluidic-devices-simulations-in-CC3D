from cc3d.core.PySteppables import *
import numpy as np

class Advection_ChemSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        field = self.field.OXYGEN
        field[60:65, 50:55, :] = 1
        self.old_field=field

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        
        field = self.field.OXYGEN
        v = 0.1 #can not be <= 1
        # field[60:65, 50:55, :] = 1 #adding material eacg step
        sumat = 0
        for i, j, k in self.every_pixel():
            cell = self.cell_field[i,j,k]
            if cell:
                if cell.type==1:#Avoiding errors with the solver making sure the wall doesn't take O2 if Wall present
                    field[i, j, k] = 0
            else: #making the cehmical to advect
                if i!= 0 and i!=99:
                    dC = -v*(self.old_field[i+1, j, k]-self.old_field[i-1, j, k])
                    field[i,j,k] += dC
                elif i==0:
                    dC = -v*(self.old_field[i+1, j, k]-self.old_field[99, j, k])
                    field[i,j,k] += dC
                elif i==99:
                    dC = -v*(self.old_field[0, j, k]-self.old_field[i-1, j, k])
                    field[i,j,k] += dC
            sumat+= field[i,j,k]
        self.old_field = field
        print(sumat)
    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
