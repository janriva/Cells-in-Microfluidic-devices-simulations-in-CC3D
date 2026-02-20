from cc3d.core.PySteppables import *
import numpy as np



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):
        
        
        
        self.plot_win = self.add_new_plot_window(title='Number of cells',
                                                 x_axis_title='MonteCarlo Step (MCS)',
                                                 y_axis_title='N Cells', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        
        self.plot_win.add_plot("Ncells", style='Lines', color='red', size=5)

        self.cell_field[:,:,0:10] = self.new_cell(self.WALL)

        for cell in self.cell_list_by_type(self.CELL):

            cell.targetVolume = 25
            cell.lambdaVolume = 2.0
            cell.lambdaVecZ = 150
            
            
    def step(self,mcs):
        
        N = 0
        if mcs>60:
            for cell in self.cell_list_by_type(self.CELL):
                N+=1
            
            self.plot_win.add_data_point("Ncells", mcs, N)
            self.plot_win.save_plot_as_data("wetable.txt",CSV_FORMAT)
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
       
        for cell in self.cell_list_by_type(self.CELL):
            cell.targetVolume += 0.5
        
        
        # arguments are (name of the data series, x, y)
        
        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)       

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume>60:
                cells_to_divide.append(cell)

        for cell in cells_to_divide:

            # self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        if self.parent_cell.type==1:
            self.child_cell.type=1
        else:
            self.child_cell.type=2

        