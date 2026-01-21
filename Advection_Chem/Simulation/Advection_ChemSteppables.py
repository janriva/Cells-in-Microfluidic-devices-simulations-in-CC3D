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
        field[60:65, 50:55, :] = 10
        self.old_field=field

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        field = self.field.OXYGEN
        v = 0.1 #No pot ser mes gran que 1 sino peta
        field[60:65, 50:55, :] = 10
        for i, j, k in self.every_pixel():
            cell = self.cell_field[i,j,k]
            if cell:
                if cell.type==1:#Avoiding errors with the solver making sure the wall doesn't take O2
                    field[i, j, k] = 0
            else:
                field[i, j, k] = -v*(field[i+1, j, k]-field[i, j, k])+self.old_field[i,j,k]
            
        self.old_field = field

    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
