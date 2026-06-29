from cc3d.core.PySteppables import *
import numpy as np



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):
        
        
        #random start height
        shape = (7,7)
        start = (40,40)
        gap = 20
        width = 5
        
        for jj in range(2):
            for kk in range(shape[1]):
                for ii in range(shape[0]):
                    
                    
                    xx = start[0]+gap*ii+width
                    zz = start[1]+gap*kk+width    
                    yy = 10*(jj+1)+np.random.rand()*15
                    
                    self.cell_field[xx:xx+width,yy:yy+width,zz:zz+width] = self.new_cell(self.NOTACTIV)
                    
        #random start position
        
        # N_cells = 98
        # width = 3
        
        # cell_centr = np.zeros((3,N_cells), dtype= np.int32)
        
        # for n in range(N_cells):
            # x = int(np.random.rand()*(self.dim.x-2*width)+width)
            # y = int(np.random.rand()*(40-2*width)+width)
            # z = int(np.random.rand()*(self.dim.z-2*width)+width)
            
            # cell_centr[:,n] = [x,y,z]

        # for nn in range(N_cells):
            # new_cell =self.new_cell(self.NOTACTIV)
            # x_cent = cell_centr[0,nn]
            # y_cent = cell_centr[1,nn]
            # z_cent = cell_centr[2,nn]
            # for ii in range(-width,width+1):   
                # for jj in range(-width,width+1):
                    # for kk in range(-width,width+1):
                        # if (ii)**2 + (jj)**2 + (kk)**2<width**2:
                            
                            # if x_cent-ii>0 and x_cent+ii<self.dim.x+1:
                                # ii = ii
                            # elif x_cent-ii<0:
                                # ii = self.dim.x+1+x_cent-ii
                                
                            # elif x_cent+ii>self.dim.x+1:
                                # ii = x_cent+ii-(self.dim.x+1)
                            
                            
                            # if y_cent-jj>0 and y_cent+jj<self.dim.y+1:
                                # jj = jj
                            # elif y_cent-jj<0:
                                # jj = self.dim.y+1+y_cent-jj
                                
                            # elif y_cent+jj>self.dim.y+1:
                                # jj = y_cent+jj-(self.dim.y+1)
                                
                                                    
                            # if z_cent-kk>0 and z_cent+kk<self.dim.z+1:
                                # kk = kk
                            # elif z_cent-kk<0:
                                # kk = self.dim.z+1+z_cent-kk
                                
                            # elif z_cent+kk>self.dim.z+1:
                                # kk = z_cent+kk-(self.dim.z+1)
                                
                            # self.cell_field[int(ii+x_cent),int(jj+y_cent),int(kk+z_cent)] = new_cell
        
        #Creació wall
        # Assegurar-se que la dim y NO és periodica
        
        # self.cell_field[:,0:10,:]=self.new_cell(self.WALL)
        
        #Creació dynabeads
        #Assegurar-se que la dim y és periodica o no
        
        N_dyna = 98
        
        dyna_centr = np.zeros((3,N_dyna), dtype= np.int32)
        
        for n in range(N_dyna):
            x = int(np.random.rand()*self.dim.x)
            y = int(np.random.rand()*10)
            z = int(np.random.rand()*self.dim.z)
            
            dyna_centr[:,n] = [x,y,z]
        
        new_cell =self.new_cell(self.WALL)
                        
        for nn in range(N_dyna):
            x_cent = dyna_centr[0,nn]
            y_cent = dyna_centr[1,nn]
            z_cent = dyna_centr[2,nn]
            for ii in range(-3,4):   
                for jj in range(-3,4):
                    for kk in range(-3,4):
                        if (ii)**2 + (jj)**2 + (kk)**2<1.5**2:
                            
                            if x_cent-ii>0 and x_cent+ii<self.dim.x+1:
                                ii = ii
                            elif x_cent-ii<0:
                                ii = self.dim.x+1+x_cent-ii
                                
                            elif x_cent+ii>self.dim.x+1:
                                ii = x_cent+ii-(self.dim.x+1)
                            
                            
                            if y_cent-jj>0 and y_cent+jj<self.dim.y+1:
                                jj = jj
                            elif y_cent-jj<0:
                                jj = self.dim.y+1+y_cent-jj
                                
                            elif y_cent+jj>self.dim.y+1:
                                jj = y_cent+jj-(self.dim.y+1)
                                
                                                    
                            if z_cent-kk>0 and z_cent+kk<self.dim.z+1:
                                kk = kk
                            elif z_cent-kk<0:
                                kk = self.dim.z+1+z_cent-kk
                                
                            elif z_cent+kk>self.dim.z+1:
                                kk = z_cent+kk-(self.dim.z+1)
                                
                            self.cell_field[int(ii+x_cent),int(jj+y_cent),int(kk+z_cent)] = new_cell
                        
                
        
        for cell in self.cell_list_by_type(self.NOTACTIV):

            cell.dict["Generation"] = 1
            cell.targetVolume = 125
            cell.lambdaVolume = 4.0
            cell.targetSurface = 1.2*cell.targetVolume**(2/3)
            cell.lambdaSurface = 4.0
            phi = np.random.rand()*2*np.pi
            theta = np.random.rand()*np.pi
            cell.lambdaVecX = 300*np.cos(phi)*np.sin(theta)
            cell.lambdaVecY = 300*np.cos(theta)
            cell.lambdaVecZ = 300*np.sin(phi)*np.sin(theta)
        
        
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
        
        self.story = []
        self.story_ind = []
        
        self.shared_steppable_vars['last_act'] = 0
        self.shared_steppable_vars['divisions_occur'] = 0
        
        self.activacions = 0

    def step(self, mcs):
    
        time_interval_act = 300 #300 per paret i 10 per dynabeads
        time_interval_move = 100
        gen = []
        deposit_str = 5 #utilitzat, 5
        
        for cell in self.cell_list_by_type(self.NOTACTIV):
            gen.append(cell.dict["Generation"])
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            common_area = neighbor_list.common_surface_area_with_cell_types(cell_type_list=[1]) 
            if np.exp(-30/(common_area+1e-12))>np.random.rand() and mcs%time_interval_act==0:
                cell.type = 3
                # cell.dict["second_activ"] = "latent"
                
                
                
                self.shared_steppable_vars['last_act'] = mcs
                self.activacions += 1
                
                
            
            if mcs % time_interval_move==0:
                phi = np.random.rand()*2*np.pi
                theta = np.random.rand()*np.pi
                cell.lambdaVecX = 300*np.cos(phi)*np.sin(theta)
                cell.lambdaVecY = 300*np.cos(theta)+deposit_str
                cell.lambdaVecZ = 300*np.sin(phi)*np.sin(theta)
            
            cell.targetVolume = 125
            cell.lambdaVolume = 3.0
            cell.targetSurface = 1.2*cell.targetVolume**(2/3)
            cell.lambdaSurface = 3.0
            

        for cell in self.cell_list_by_type(self.EXAUST):
            gen.append(cell.dict["Generation"])
            
            cell.targetVolume = 195
            cell.lambdaVolume = 3.0
            cell.targetSurface = 1.6*cell.targetVolume**(2/3)
            cell.lambdaSurface = 3.0
            l = 2*(3*cell.targetVolume/(4*np.pi))**(1/3)
            self.lengthConstraintPlugin.setLengthConstraintData(cell,2,1.1*l,0.99*l)
            
            
            if mcs % time_interval_move==0:
                phi = np.random.rand()*2*np.pi
                theta = np.random.rand()*np.pi
                cell.lambdaVecX = 250*np.cos(phi)*np.sin(theta)
                cell.lambdaVecY = 250*np.cos(theta) +deposit_str
                cell.lambdaVecZ = 250*np.sin(phi)*np.sin(theta)
            
        
            #Condicions si es poden reactivar
            
            # if cell.dict["Generation"] > 7 and cell.dict["second_activ"] != "exaust":
                    # cell.dict["second_activ"] = "exaust"
            
            
            # if cell.dict["second_activ"] == "latent":
                # cell.targetVolume = 195
                # cell.lambdaVolume = 3.0
                # cell.targetSurface = 1.6*cell.targetVolume**(2/3)
                # cell.lambdaSurface = 3.0
                # # l = 2*(3*cell.targetVolume/(4*np.pi))**(1/3)
                # # self.lengthConstraintPlugin.setLengthConstraintData(cell,2,1.1*l,0.99*l)
                
                # neighbor_list = self.get_cell_neighbor_data_list(cell)
                # common_area = neighbor_list.common_surface_area_with_cell_types(cell_type_list=[1])
                                
                # if common_area>3 and np.random.rand()<0.25:
                    # cell.dict["second_activ"] = "activa"
                    
            # elif cell.dict["second_activ"] == "activa":
                # cell.targetVolume += 1
                # cell.lambdaSurface = 1.5
                # cell.targetSurface = 6*cell.targetVolume**(2/3)
                
            # elif cell.dict["second_activ"] == "exaust":
                # cell.targetVolume = 195
                # cell.lambdaVolume = 3.0
                # cell.targetSurface = 1.6*cell.targetVolume**(2/3)
                # cell.lambdaSurface = 3.0
                
                    
                
        for cell in self.cell_list_by_type(self.ACTIV):
            gen.append(cell.dict["Generation"])
            cell.lambdaSurface = 1.5
            cell.targetVolume += 0.1
            cell.targetSurface = 8*cell.targetVolume**(2/3)
            # self.lengthConstraintPlugin.setLengthConstraintData(cell,2,15)
            
            
            if mcs % time_interval_move==0:
                phi = np.random.rand()*2*np.pi
                theta = np.random.rand()*np.pi
                cell.lambdaVecX = 50*np.cos(phi)*np.sin(theta)
                cell.lambdaVecY = 50*np.cos(theta)+deposit_str
                cell.lambdaVecZ = 50*np.sin(phi)*np.sin(theta)
            
            
        self.plot_win.add_histogram(plot_name='Hist 1', value_array=gen, number_of_bins=max(gen))
        gen = np.array(gen)
        
        gen_max = np.max(gen)
        counts = np.zeros(gen_max)
        counts_2gen = np.zeros(gen_max)
        counts_gen_2gen = np.zeros(gen_max)
        
        for ii in range(gen_max):
            counts[ii] = np.count_nonzero(gen==(ii+1))
            counts_2gen[ii] = counts[ii]/(2**(ii))
            counts_gen_2gen[ii] = ii*counts[ii]/(2**(ii))
            
        proliferationIndex = np.sum(counts_gen_2gen)/(self.starting_cells-counts[0])
        # proliferationIndex = self.shared_steppable_vars['divisions_occur']/(self.starting_cells-counts[0])
        replicationIndex = np.sum(counts[1:])/(self.starting_cells-counts[0])
        expansionIndex = np.sum(counts)/self.starting_cells
        
        freq_save = 50
        
        if mcs%freq_save == 0:
            self.story.append(counts)
            self.story_ind.append([proliferationIndex,replicationIndex,expansionIndex])
        
        
            with open("Ngens_7_2.5_diffgrow_dyna.txt",'w') as file:
                
                for tt in range(len(self.story)):
                    file.write("{}\t".format(tt*freq_save))
                    
                    c = self.story[tt]
                    
                    for ii in range(np.size(c)):
                        
                        file.write("{}\t".format(c[ii]))
                    
                    file.write("\n")
                    
            with open("Index_story_7_2.5_diffgrow_dyna.txt",'w') as file:
                
                for tt in range(len(self.story_ind)):
                    file.write("{}\t".format(tt*freq_save))
                    
                    ind = self.story_ind[tt]
                    
                    for ii in range(np.size(ind)):
                        
                        file.write("{}\t".format(ind[ii]))
                    
                    file.write("\n")
        
        
        # if mcs-self.shared_steppable_vars['last_act']>1000 and mcs>15000:
        if mcs>160000:
        # if self.activacions>90:
            print(mcs)
            self.stop_simulation()

        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.ACTIV):
            if cell.volume>300:
                cells_to_divide.append(cell)
                self.shared_steppable_vars['last_act'] = mcs
                self.shared_steppable_vars['divisions_occur'] += 1
        
        #reactivation
        # for cell in self.cell_list_by_type(self.EXAUST):
            # if cell.volume>320:
                # cells_to_divide.append(cell)
                # self.shared_steppable_vars['last_act'] = mcs
                # cell.dict["second_activ"] = "exaust"

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
        
        
        
        if self.parent_cell.type == 3 :
            
            # hand_prob = [0,0.15,0.2,0.3,0.3,0.35,0.6,1]
        
            # boltz_prob = hand_prob[int(self.parent_cell.dict["Generation"]-1)]
            boltz_prob = np.exp(-7/np.exp(self.parent_cell.dict["Generation"]/2.5))
    
            exaustation = np.random.rand()<boltz_prob or self.parent_cell.dict["Generation"]>7
            if exaustation:
                self.parent_cell.type = 4
            
            exaustation = np.random.rand()<boltz_prob or self.parent_cell.dict["Generation"]>7
            if exaustation:
                self.child_cell.type = 4

        