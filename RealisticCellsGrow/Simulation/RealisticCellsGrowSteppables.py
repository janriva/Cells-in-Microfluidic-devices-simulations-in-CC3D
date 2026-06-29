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
        
        
        self.plot_win2 = self.add_new_plot_window(title='Geometric parameters',
                                                 x_axis_title='MonteCarlo Step (MCS)',
                                                 y_axis_title='Contact_angle/height/radius', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        self.plot_win2.add_plot("ContAngle", style = 'Lines', color = 'green', size =5)
        
        self.plot_win2.add_plot("Height", style = 'Lines', color = 'red', size =5)
        self.plot_win2.add_plot("Radius", style = 'Lines', color = 'blue', size =5)
        
        
        
        # flat wall
        self.cell_field[:,0:100,:]=self.new_cell(self.WALL)
        
        
        
        #circle
        # radius = 250
        # cent_x = (self.dim.x-1)/2
        # cent_y = 100+radius
        # cent_z = (self.dim.z-1)/2
        # newcell = self.new_cell(self.WALL)       
        # for i,j,k in self.every_pixel():
            # if (i-cent_x)**2 + (k-cent_z)**2+ (j-cent_y)**2> radius**2:
                # self.cell_field[i,j,k] = newcell
        

        for cell in self.cell_list_by_type(self.CELL):

            cell.targetVolume = 45
            cell.lambdaVolume = 4.0
            cell.lambdaVecZ = 15
            cell.dict['Sulten'] = 150
            
            
            
        # self.field.O2[:,:,100:] = 10
        # self.field.Glu[:,:,:100] = 10
        
        self.N_cells = []
        self.angle = []
        self.height = []
        self.radius = []
        
    def step(self, mcs):
        
        # if mcs ==2:
            # self.change_number_of_work_nodes(6)
        
        for cell in self.cell_list_by_type(self.WALL):
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            common_area = neighbor_list.common_surface_area_with_cell_types(cell_type_list=[2])
            
        N=0        
        for cell in self.cell_list_by_type(self.CELL):
            N+=1
        
        #3D
        # tot_vol=0
        # for cell in self.cell_list_by_type(self.CELL):
            # tot_vol+=cell.volume
        
        
        # r_2 = common_area/np.pi
        
        # res_h = optimize.root(lambda x: x**3 +3*r_2*x-6*tot_vol/np.pi, 20)
        
        # cont_angle = 2*np.arctan(res_h.x/np.sqrt(r_2))*180/np.pi 
        
        
        #2D coment for circle
        for kk in range(self.dim.y):
            cell_not_found = 0
            for ii in range(self.dim.x):
                cell = self.cell_field[ii,kk,0]
                if cell:
                    break                    
                else:
                    cell_not_found = ii
                    
            if cell_not_found ==  self.dim.x-1:
                h = kk-100
                break
        
                
        r = common_area/2
        cont_angle = 2*np.arctan(h/r)*180/np.pi
        
        
        if mcs>300:
            # self.stop_simulation()
            
            self.N_cells.append(N)
            self.angle.append(cont_angle)
            self.height.append(h)
            self.radius.append(r)
            
            with open("cont_angle20.txt", 'w') as file:
                file.write("mcs\tN_cells\tangle\theight\tradius\n")
                for ii in range(len(self.N_cells)):
                    file.write("{}\t{}\t{}\t{}\t{}\n".format(ii+300,self.N_cells[ii],self.angle[ii],self.height[ii],self.radius[ii]))
            
            #self.plot_win.add_data_point("Ncells", mcs, len(self.cell_list_by_type(self.CELL)))
            #self.plot_win.save_plot_as_data("colony_growth0.txt",CSV_FORMAT)
            
            #self.plot_win2.add_data_point("ContAngle", mcs, cont_angle)
            #self.plot_win2.add_data_point("Height", mcs, h)
            #self.plot_win2.add_data_point("Radius", mcs, r)
            #self.plot_win2.save_plot_as_data("cont_angle_CG0.txt",CSV_FORMAT)
            
            #Circle
            # with open("cont_angle0.txt", 'w') as file:
                # file.write("mcs\tN_cells\n")
                # for ii in range(len(self.N_cells)):
                    # file.write("{}\t{}\n".format(ii+300,self.N_cells[ii]))
                    
        elif mcs == 300:
            # flat
            self.field.O2[:,:,:] = 0.6 #e-12 mg/px³
            self.field.Glu[:,:,:] = 0.6 #e-12 mg/px³
            
            # circle
            # radius = 250
            # cent_x = (self.dim.x-1)/2
            # cent_y = (self.dim.y-1)/2
            # cent_z = 100+radius
            # for i,j,k in self.every_pixel():
                # if (i-cent_x)**2 + (k-cent_z)**2+ (j-cent_y)**2> radius**2:
                    # self.field.Glu[i,j,k] = 16
                # else:
                    # self.field.O2[i,j,k] = 16
                
        elif mcs<300:
            self.field.O2[:,:,:] = 0
            self.field.Glu[:,:,:] = 0
            
            
        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        
    
        #print("MCS = ", mcs)

        if mcs>300 and mcs%60==0:
        
            Kg_grow = 4e-2 #e-12 mg/px³ 
            Kg_upt = 1.6 # e-12 mg/px³
            Ko = 0.28 # e-12 mg/px³
            
            
            lam_g_aer = 0.6
            lam_g_ana = 0.3
            
            q_g_aer = 833 #e-12 mg/cell 60mcs
            q_g_ana = 833 #e-12 mg/cell 60mcs
            q_o_g = 833 #e-12 mg/cell 60mcs
            Q_main = 15
            
            secretor_g = self.get_field_secretor("Glu")
            secretor_o = self.get_field_secretor("O2")
            
            for cell in self.cell_list_by_type(self.CELL):
                
                glu_seen = secretor_g.amountSeenByCell(cell)
                o2_seen = secretor_o.amountSeenByCell(cell)
                
                theta_g_grow = glu_seen/(Kg_grow+glu_seen)
                theta_g_upt = glu_seen/(Kg_upt+glu_seen)
                theta_o = o2_seen/(Ko+o2_seen)
                
                lam1 = lam_g_aer*theta_g_grow*theta_g_upt*theta_o
                lam2 = lam_g_ana*theta_g_grow*theta_g_upt*(1-theta_o)
                
                up_o2 = q_o_g*lam1
                up_glu = q_g_aer*lam1+q_g_ana*lam2+Q_main
                
                o2_upt = secretor_o.uptakeOutsideCellAtBoundaryTotalCount(cell, up_o2/cell.surface, 1)
                glu_upt = secretor_g.uptakeOutsideCellAtBoundaryTotalCount(cell, up_glu/cell.surface, 1)
                
                if -glu_upt.tot_amount<Q_main:
                    cell.dict['Sulten'] -= Q_main/(-glu_upt.tot_amount+Q_main)
                elif -glu_upt.tot_amount>Q_main and cell.dict['Sulten']<100:
                    ratio = glu_upt.tot_amount/Q_main
                    if ratio + cell.dict['Sulten']<150:
                        cell.dict['Sulten'] += ratio
                    else:
                        cell.dict['Sulten'] = 150
                        cell.targetVolume += (lam1+lam2)*np.sqrt(cell.volume/np.pi)
                        
                else:                
                    cell.targetVolume += (lam1+lam2)*np.sqrt(cell.volume/np.pi)

                
                if cell.dict['Sulten']<=0:
                    cell.dict['Sulten'] = -10000
                    cell.targetVolume -= 1
                    if cell.volume<=2:
                        self.delete_cell(cell)
        
    
        

        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume>80:
                cells_to_divide.append(cell)

        for cell in cells_to_divide:

            self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 

        
