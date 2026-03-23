from cc3d.core.PySteppables import *
import numpy as np
from scipy import optimize



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
        
        
        
        #flat wall
        self.cell_field[:,:,0:100]=self.new_cell(self.WALL)
        
        #circle
        # radius = 150
        # cent_x = (self.dim.x-1)/2
        # cent_y = (self.dim.y-1)/2
        # cent_z = 100+radius
        # newcell = self.new_cell(self.WALL)       
        # for i,j,k in self.every_pixel():
            # if (i-cent_x)**2 + (k-cent_z)**2+ (j-cent_y)**2> radius**2:
                # self.cell_field[i,j,k] = newcell
        

        for cell in self.cell_list_by_type(self.CELL):

            cell.targetVolume = 25
            cell.lambdaVolume = 4.0
            cell.lambdaVecZ = 50
            
        # self.field.O2[:,:,100:] = 10
        # self.field.Glu[:,:,:100] = 10
            
    def step(self, mcs):
        
        for cell in self.cell_list_by_type(self.WALL):
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            common_area = neighbor_list.common_surface_area_with_cell_types(cell_type_list=[2])
        
        #3D
        # tot_vol=0
        # for cell in self.cell_list_by_type(self.CELL):
            # tot_vol+=cell.volume
        
        
        # r_2 = common_area/np.pi
        
        # res_h = optimize.root(lambda x: x**3 +3*r_2*x-6*tot_vol/np.pi, 20)
        
        # cont_angle = 2*np.arctan(res_h.x/np.sqrt(r_2))*180/np.pi 
        
        
        # #2D coment for circle
        for kk in range(self.dim.z):
            cell_not_found = 0
            for ii in range(self.dim.x):
                cell = self.cell_field[ii,0,kk]
                if cell:
                    break                    
                else:
                    cell_not_found = ii
                    
            if cell_not_found ==  self.dim.x-1:
                h = kk-100
                break
                
        
        r = common_area/2
        cont_angle = 2*np.arctan(h/r)*180/np.pi
        
        
        if mcs>400:        
            self.plot_win.add_data_point("Ncells", mcs, len(self.cell_list_by_type(self.CELL)))
            self.plot_win.save_plot_as_data("colony_growth.txt",CSV_FORMAT)
            
            self.plot_win2.add_data_point("ContAngle", mcs, cont_angle)
            self.plot_win2.add_data_point("Height", mcs, h)
            self.plot_win2.add_data_point("Radius", mcs, r)
            self.plot_win2.save_plot_as_data("cont_angle_CG.txt",CSV_FORMAT)
        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)
        
    def step(self, mcs):
                
        print("MCS = ", mcs)

        if mcs>400:
            Ka = 5 #mM
            Kg = 20e-3 #mM
            Ko = 0.1e-3 #mM
            
            lam_a_aer = 0.9
            lam_g_aer = 0.6
            lam_g_ana = 0.4
            
            q_g_aer = 1.1
            q_g_ana = 2.8
            q_o_g = 2.2
            q_o_a = 2.2
            q_a_aer = 3.3
            
            p_a_ana = 16
            p_a_aer = 3
            
            secretor_a = self.get_field_secretor("Ac")
            secretor_g = self.get_field_secretor("Glu")
            secretor_o = self.get_field_secretor("O2")
            
            
            
            for cell in self.cell_list_by_type(self.CELL):
                
                ac_seen = secretor_a.amountSeenByCell(cell)
                glu_seen = secretor_g.amountSeenByCell(cell)
                o2_seen = secretor_o.amountSeenByCell(cell)
                
                theta_g = glu_seen/(Kg+glu_seen)
                theta_a = ac_seen/(Ka+ac_seen)
                theta_o = o2_seen/(Ko+o2_seen)
                
                lam1 = lam_g_aer*theta_g*theta_o
                lam2 = lam_g_ana*theta_g*(1-theta_o)
                lam3 = lam_a_aer*theta_a*(1-theta_g)*theta_o
                
                          
                up_o2 = q_o_a*lam3 + q_o_g*lam1
                up_ac = q_a_aer*lam3
                up_glu = q_g_aer*lam1+q_g_ana*lam2
                
                sec_ac = p_a_aer*lam1+p_a_ana*lam2
                
                secretor_a.uptakeOutsideCellAtBoundaryTotalCount(cell, up_ac, 1)
                secretor_o.uptakeOutsideCellAtBoundaryTotalCount(cell, up_o2, 1)
                secretor_g.uptakeOutsideCellAtBoundaryTotalCount(cell, up_glu, 1)
                
                secretor_a.secreteOutsideCellAtBoundary(cell, sec_ac)
                
                cell.targetVolume += (lam1+lam2+lam3)*np.sqrt(cell.volume)
                
            
        elif mcs == 400:
            #flat
            self.field.O2[:,:,100:] = 1000
            self.field.Glu[:,:,:100] = 1000
            
            # circle
            # radius = 150
            # cent_x = (self.dim.x-1)/2
            # cent_y = (self.dim.y-1)/2
            # cent_z = 100+radius
            # it = 0
            # for i,j,k in self.every_pixel():
                # it+=1
                # if (i-cent_x)**2 + (k-cent_z)**2+ (j-cent_y)**2> radius**2:
                    # self.field.Glu[i,j,k] = 10
                # else:
                    # self.field.O2[i,j,k] = 10
                
        elif mcs<400:
            self.field.O2[:,:,:] = 0
            self.field.Glu[:,:,:] = 0
            

        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume>50:
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
        