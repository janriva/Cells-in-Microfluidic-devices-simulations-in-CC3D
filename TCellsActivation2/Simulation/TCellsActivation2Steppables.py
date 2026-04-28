from cc3d.core.PySteppables import *
import numpy as np



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):
        self.cell_field[:,0:50,:]=self.new_cell(self.WALL)
        
        for cell in self.cell_list_by_type(self.NOTACTIV):

            cell.dict["Generation"] = 1
            cell.targetVolume = 30
            cell.lambdaVolume = 4.0
            cell.targetSurface = 1.2*np.pi*cell.targetVolume**(1/2)
            cell.lambdaSurface = 4.0
        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)
        
    def start(self):
        self.plot_win = self.add_new_plot_window(title='Histogram of Cell Generations', x_axis_title='Generation',
                                                 y_axis_title='Number of cells')
                                                 
        self.plot_win.add_histogram_plot(plot_name='Hist 1', color='green', alpha=100)
        
        self.starting_cells = 0
        
        for cell in self.cell_list_by_type(self.NOTACTIV):
            self.starting_cells += 1

    def step(self, mcs):
        
    
        time_interval_act = 300
        time_interval_move = 50
        gen = []
        for cell in self.cell_list_by_type(self.NOTACTIV):
            gen.append(cell.dict["Generation"])
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            common_area = neighbor_list.common_surface_area_with_cell_types(cell_type_list=[1]) 
            
            if np.exp(-8/(common_area+1e-12))>np.random.rand() and mcs%time_interval_act==0:
                cell.type = 3
                
            
            if mcs % time_interval_move:
                angle = np.random.rand()*2*np.pi
                cell.lambdaVecX = 300*np.cos(angle)
                cell.lambdaVecY = 300*np.sin(angle)
            
            cell.targetVolume = 30
            cell.lambdaVolume = 4.0
            cell.targetSurface = 1.2*np.pi*cell.targetVolume**(1/2)
            cell.lambdaSurface = 4.0
            

        for cell in self.cell_list_by_type(self.EXAUST):
            gen.append(cell.dict["Generation"])
            cell.targetVolume = 40
            cell.lambdaVolume = 4.0
            cell.targetSurface = 1.4*np.pi*cell.targetVolume**(1/2)
            cell.lambdaSurface = 6.0
            self.lengthConstraintPlugin.setLengthConstraintData(cell,4,np.sqrt(4*cell.targetVolume/np.pi))
            
            if mcs % time_interval_move:
                angle = np.random.rand()*2*np.pi
                cell.lambdaVecX = 200*np.cos(angle)
                cell.lambdaVecY = 200*np.sin(angle)
                
        for cell in self.cell_list_by_type(self.ACTIV):
            gen.append(cell.dict["Generation"])
            cell.lambdaSurface = 1.0
            cell.targetVolume += 0.1
            cell.targetSurface = 2*np.pi*cell.targetVolume**(1/2)
            self.lengthConstraintPlugin.setLengthConstraintData(cell,4,15)
            
            
            if mcs % time_interval_move:
                angle = np.random.rand()*2*np.pi
                cell.lambdaVecX = 300*np.cos(angle)
                cell.lambdaVecY = 300*np.sin(angle)
            
            
            
        self.plot_win.add_histogram(plot_name='Hist 1', value_array=gen, number_of_bins=max(gen))
       
       
        if mcs>6000:
            gen = np.array(gen)
            gen_max = np.max(gen)
            
            counts = np.zeros(gen_max)
            counts_2gen = np.zeros(gen_max)
            
            for ii in range(gen_max):
                counts[ii] = np.count_nonzero(gen==(ii+1))
                counts_2gen[ii] = counts[ii]/(2**(ii))
            
            proliferationIndex = np.sum(counts)/np.sum(counts_2gen)
            replicationIndex = np.sum(counts[1:])/(self.starting_cells-counts[0])
            expansionIndex = np.sum(counts)/self.starting_cells
            
            print("Proliferation Index = ", proliferationIndex)
            print("Replication Index = ", replicationIndex)
            print("Expansion Index = ", expansionIndex)
            
            with open("gen4.txt", 'w') as file:
                for gg in gen:
                    
                    file.write("{}\n".format(gg))
                    
                    
            self.stop_simulation()
            
        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)
        
    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.ACTIV):
            if cell.volume>50:
                cells_to_divide.append(cell)

        for cell in cells_to_divide:

            # self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            cell.dict["Generation"] += 1
            self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()

        # boltz_prob = np.exp(-3/self.parent_cell.dict["Generation"])
        boltz_prob = np.exp(-4/np.exp(self.parent_cell.dict["Generation"]/3))
        # boltz_prob = 2*self.parent_cell.dict["Generation"]/(self.parent_cell.dict["Generation"]+10)
        # boltz_prob = np.exp(-self.parent_cell.dict["Generation"]/6)
        exaustation = np.random.rand()<boltz_prob or self.parent_cell.dict["Generation"]>7
        # exaustation = np.random.rand()>boltz_prob
        if exaustation:
            self.parent_cell.type = 4
        
        exaustation = np.random.rand()<boltz_prob or self.parent_cell.dict["Generation"]>7
        if exaustation:
            self.child_cell.type = 4

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        

        