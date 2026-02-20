from cc3d.core.PySteppables import *
import numpy as np



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):
        
        self.plot_win = self.add_new_plot_window(title='Volume/Complexity',
                                                 x_axis_title='Volume',
                                                 y_axis_title='Complexity', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        
        self.plot_win.add_plot("VolComp", style='Dots', color='green', size=5)
        self.plot_win.save_plot_as_data("plots.txt",CSV_FORMAT)
        
        
        self.flux = 1
        
        wallWidth  =  2
        circleRadius= 20
        N_porus = 30
        dim = self.dim.x
        pics = 2
        sig = 50
        
        #Posicions depenent de distribució de probabilitat
        dist_prob=np.zeros(dim)
        for pp in range(pics):
            # dist_prob += np.sinc(2*np.pi*(np.arange(0,dim)-pp*dim/pics))
                        
            dist_prob += np.exp(-(np.arange(0, dim)-(pp+1/2)*dim/pics)**2/(2*sig**2))
            
        dist_prob[:5] = 0
        dist_prob[-5:]=0
        dist_prob = dist_prob/dist_prob.sum()
        pos_cent_x = np.random.choice(self.dim.x,size=N_porus, p = dist_prob,replace=False)
        pos_cent_y = np.random.choice(self.dim.y,size=N_porus, p = dist_prob,replace=False)
        pos_cent_z = np.random.choice(self.dim.z,size=N_porus, p = dist_prob,replace=False)
        
               
        #Posicions aleatòries amb distribuicó uniforme
        # pos_cent_x = np.random.randint(0,self.dim.x, size = N_porus)
        # pos_cent_y = np.random.randint(0,self.dim.y, size = N_porus)
        
        newCell = self.new_cell(self.WALL)
        self.wall_points = []
        
        for i,j,k in self.every_pixel():
            dins = False
            if i==0 and j==0 and k==0:
                continue
            for nn in range(N_porus):
                centx = int(pos_cent_x[nn])
                centy = int(pos_cent_y[nn])
                centz = int(pos_cent_z[nn])
                if ((i-centx)**2 + (j-centy)**2+(k-centz)**2)<(circleRadius)**2:
                    dins = True
                    break
            if not(dins):
                self.cell_field[i,j,k] = newCell
                self.wall_points.append([i,j,k,0])
                   
        
        for nn in range(N_porus):
            newCell2 = self.new_cell(self.CELL)
            centx = int(pos_cent_x[nn])
            centy = int(pos_cent_y[nn])
            centz = int(pos_cent_z[nn])
            self.cell_field[centx-3:centx+3, centy-3:centy+3,centz-3:centz+3] = newCell2
                
        
        # for nn1 in range(N_porus):
            # newCell2 = self.new_cell(self.CELL)
            # # if nn1%2 ==0 :
            # centx = int(pos_cent_x[nn1])
            # centy = int(pos_cent_y[nn1])
            # centz = int(pos_cent_z[nn1])
            # self.cell_field[centx-3:centx+3, centy-3:centy+3,centz-3:centz+3] = newCell2
                
            # for dd in range(wallWidth):
                # R = circleRadius+dd
                # for ang in np.linspace(0,2*np.pi, 4*(int(R))):
                    # for theta in np.linspace(0,np.pi, 4*(int(R))):
                        
                        # dins = False
                        # px = int(centx+R* np.cos(ang)*np.sin(theta))
                        # py = int(centy+R* np.sin(ang)*np.sin(theta))
                        # pz = int(centz+R* np.cos(theta))

                        # if (px+2<= self.dim.x-1 and px>=0) and (py+2<=self.dim.y-1 and py>=0) and (pz+2<=self.dim.z-1 and pz>=0):
                            # for nn2 in range(N_porus):
                                # if nn1!=nn2:
                                    # if ((px-pos_cent_x[nn2])**2 + (py-pos_cent_y[nn2])**2+(pz-pos_cent_z[nn2])**2)<(circleRadius)**2:
                                        # dins = True
                                        # break
                            # if not(dins):
                                # self.cell_field[px:px+2,py:py+2,pz:pz+2] = newCell
                                
        
        field = self.field.Nutr
        field[:,:,:]=1 #aliment inicial
           

        for cell in self.cell_list:

            cell.targetVolume = 350
            cell.lambdaVolume = 2.0
        
    def step(self,mcs):
        
        self.plot_win.erase_all_data()
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume < 10:
                self.delete_cell(cell)
                continue
            #Wall degradetion    
            # secretor = self.get_field_secretor("Degr")
            # secretor.secreteOutsideCellAtBoundary(cell, 0.7)            
            
            comp = cell.dict["complexity"]
            vol = cell.volume
            self.plot_win.add_data_point("VolComp", vol, comp)
            
            cell.lambdaVecY = 500
        
        #Wall degradetion
        # field = self.field.Degr
        # nn = 0
        # for pp in self.wall_points:
            # cell = self.cell_field[pp[0],pp[1],pp[2]]
            # if cell:
                # if cell.type ==1:
                    # quant = field[pp[0],pp[1],pp[2]]
                    # pp[3] += quant
                    # field[pp[0],pp[1],pp[2]] = 0
                    # if pp[3] > 100:
                        # self.cell_field[pp[0],pp[1],pp[2]] = None
            # else:
                # self.wall_points.pop(nn)
            # nn +=1
        # if mcs%10 == 0:
            # print(nn)
        
        
        field = self.field.Nutr
        # field[:,:,:] = 1
        field[0,:,:] = 1
        
        
        
        
        self.plot_win.save_plot_as_data("plots.txt",CSV_FORMAT)
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)
        
    def start(self):
        for cell in self.cell_list_by_type(self.CELL):
            cell.dict["uptake"] = 0
            cell.dict["complexity"] = 0

    def step(self, mcs):          
        
        secretor = self.get_field_secretor("Nutr")
        for cell in self.cell_list_by_type(self.CELL):
            rat= 2-np.exp(-cell.dict["complexity"])
            # arguments are: cell, max uptake, relative uptake
            # Um = secretor.uptakeInsideCellTotalCount(cell, 0.05*rat, 0.2)
            Um = secretor.uptakeOutsideCellAtBoundaryTotalCount(cell, 0.05*rat, 1)
            
            
            cell.dict["uptake"] += np.abs(Um.tot_amount)
            
            if cell.dict["uptake"]>0.1:
                gr_co = np.random.randint(0,2)
                if gr_co == 0:                    
                    cell.targetVolume += 0.5*cell.dict["uptake"]
                    cell.dict["uptake"] = 0
                elif gr_co == 1:
                    cell.dict["complexity"] += cell.dict["uptake"]
                    cell.dict["uptake"] = 0
            

        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        # field = self.field.CHEMICAL_FIELD_NAME
        
        # for cell in self.cell_list:
            # concentrationAtCOM = field[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]

            # # you can use here any fcn of concentrationAtCOM
            # cell.targetVolume += 0.01 * concentrationAtCOM       

        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume>560:
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
        
        self.parent_cell.dict["complexity"] /= 2.0
        self.child_cell.dict["complexity"] /= 2.0

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        # if self.parent_cell.type==1:
            # self.child_cell.type=1
        # else:
            # self.child_cell.type=1

        