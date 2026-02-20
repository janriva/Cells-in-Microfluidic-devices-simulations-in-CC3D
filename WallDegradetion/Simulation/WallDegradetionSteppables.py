from cc3d.core.PySteppables import *
import numpy as np

class WallDegradetionSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        
        for cell in self.cell_list_by_type(self.CELL):
            cell.targetVolume = 20
            cell.lambdaVolume = 4.0
            
        self.cell_field[0:20,:,:] = self.new_cell(self.WALL)
        
        self.wall_points = []
        
        for ii, jj, kk in self.every_pixel():
            cell = self.cell_field[ii,jj,kk]
            if cell:
                if cell.type==1:
                    self.wall_points.append([ii,jj,kk,0])
        print(self.wall_points)
    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """

        for cell in self.cell_list_by_type(self.CELL):
            # Make sure Secretion plugin is loaded
            # make sure this field is defined in one of the PDE solvers
            # you may reuse secretor for many cells. Simply define it outside the loop
            secretor = self.get_field_secretor("Degr")
            secretor.secreteOutsideCellAtBoundary(cell, 0.1)
            # tot_amount = secretor.secreteOutsideCellAtBoundaryTotalCount(cell, 300).tot_amount
        
        
        field = self.field.Degr
        nn = 0
        for pp in self.wall_points:
            cell = self.cell_field[pp[0],pp[1],pp[2]]
            if cell:
                if cell.type ==1:
                    quant = field[pp[0],pp[1],pp[2]]
                    pp[3] += quant
                    field[pp[0],pp[1],pp[2]] = 0
                    if pp[3] > 100:
                        self.cell_field[pp[0],pp[1],pp[2]] = None
            else:
                self.wall_points.pop(nn)
            nn +=1
    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
