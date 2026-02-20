from cc3d.core.PySteppables import *
import numpy as np

class ProvesCanviCellsSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        
        newCell = self.new_cell(self.WALL)
        self.cell_field[0:25,0:50,0:50] = newCell
        
        for cell in self.cell_list_by_type(self.CELL):

            cell.targetVolume = 30
            cell.lambdaVolume = 4.0
            cell.lambdaVecX = 80

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        
        
        for cell in self.cell_list_by_type(self.CELL):
            detect = False
            for neighbor, com_surf in self.get_cell_neighbor_data_list(cell):
                if neighbor:
                    if neighbor.type == 1:
                        detect = True
                        break
            
            if detect and mcs%10 == 0:
                xCOM = cell.xCOM
                yCOM = cell.yCOM
                zCOM = cell.zCOM
                
                if xCOM-5<0:
                    esq = xCOM
                else:
                    esq = 5
                if xCOM+5>self.dim.x-1:
                    dret = -xCOM+self.dim.x-1
                else:
                    dret = 5
                if yCOM-5<0:
                    baix = yCOM
                else:
                    baix = 5
                if yCOM+5>self.dim.y-1:
                    dalt = -yCOM+self.dim.y-1
                else:
                    dalt = 5
                if zCOM-5<0:
                    prop = zCOM
                else:
                    prop = 5
                if zCOM+5>self.dim.z-1:
                    lluny = -zCOM+self.dim.z-1
                else:
                    lluny = 5
                    
                    
                point = 5    
                
                dist_old = 3*self.dim.x**2
                for ii in range(int(xCOM-esq),int(xCOM+dret)):
                    for jj in range(int(yCOM-baix),int(yCOM+dalt)):
                        for kk in range(int(yCOM-baix),int(yCOM+dalt)):
                            px = self.cell_field[ii,jj,kk]
                            if px:
                                if px.type == 1:
                                    dist = (ii-xCOM)**2+(jj-yCOM)**2+(kk-zCOM)**2
                                    
                                    if dist<dist_old:
                                        point = (ii,jj,kk)
                                        dist_old=dist
                if point!=5:
                    
                    self.cell_field[point[0],point[1],point[2]] = None
                
    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
