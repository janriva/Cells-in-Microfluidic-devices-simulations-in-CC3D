from cc3d.core.PySteppables import *
import numpy as np



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):

        #creating the plots
        self.plot_win = self.add_new_plot_window(title='Volume/Complexity',
                                                 x_axis_title='Volume',
                                                 y_axis_title='Complexity', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        
        self.plot_win.add_plot("VolComp", style='Dots', color='green', size=5)
        self.plot_win.save_plot_as_data("plots.txt",CSV_FORMAT)
        
        
        self.flux = 1 #1 for flux, 0 for not flux

        #porus parameters
        wallWidth  =  2
        circleRadius= 20
        N_porus = 30
        dim = self.dim.x
        #probability distribution parameters
        pics = 2
        sig = 50
        
        #creating the probability distribution (PD)
        dist_prob=np.zeros(dim)
        for pp in range(pics):
            # dist_prob += np.sinc(2*np.pi*(np.arange(0,dim)-pp*dim/pics))
                        
            dist_prob += np.exp(-(np.arange(0, dim)-(pp+1/2)*dim/pics)**2/(2*sig**2))
            
        dist_prob[:5] = 0
        dist_prob[-5:]=0
        dist_prob = dist_prob/dist_prob.sum()

        #Selecting the porus positions based on PD
        pos_cent_x = np.random.choice(self.dim.x,size=N_porus, p = dist_prob,replace=False)
        pos_cent_y = np.random.choice(self.dim.y,size=N_porus, p = dist_prob,replace=False)
        pos_cent_z = np.random.choice(self.dim.z,size=N_porus, p = dist_prob,replace=False)
        
               
        #If we want uniform distribution use next:
        # pos_cent_x = np.random.randint(0,self.dim.x, size = N_porus)
        # pos_cent_y = np.random.randint(0,self.dim.y, size = N_porus)
        # pos_cent_z = np.random.randint(0,self.dim.z, size = N_porus)

        #Creating the porus media with one big wall cell
        newCell = self.new_cell(self.WALL)
        self.wall_points = []
        
        for i,j,k in self.every_pixel():
            dins = False
            if i==0 and j==0 and k==0:
                continue
            #cheking if the point it's inside a porus
            for nn in range(N_porus):
                centx = int(pos_cent_x[nn])
                centy = int(pos_cent_y[nn])
                centz = int(pos_cent_z[nn])
                if ((i-centx)**2 + (j-centy)**2+(k-centz)**2)<(circleRadius)**2:
                    dins = True
                    break
            #if not inside create the wall and add the point to the list to keep track of it
            if not(dins):
                self.cell_field[i,j,k] = newCell
                self.wall_points.append([i,j,k,0])
                   
        #adding cells inside the centers of the porus
        for nn in range(N_porus):
            newCell2 = self.new_cell(self.CELL)
            centx = int(pos_cent_x[nn])
            centy = int(pos_cent_y[nn])
            centz = int(pos_cent_z[nn])
            self.cell_field[centx-3:centx+3, centy-3:centy+3,centz-3:centz+3] = newCell2
                
        
                                     
        #Creating initial nutrient field
        field = self.field.Nutr
        field[:,:,:]=1
           
        #setting cells parameters
        for cell in self.cell_list:

            cell.targetVolume = 350
            cell.lambdaVolume = 2.0
        
    def step(self,mcs):

        self.plot_win.erase_all_data()
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume < 10:
                self.delete_cell(cell)
                continue
            #uncoment for Wall degradetion    
            # secretor = self.get_field_secretor("Degr")
            # secretor.secreteOutsideCellAtBoundary(cell, 0.7)            

            #saving complexity and volume parameters in the plot
            comp = cell.dict["complexity"]
            vol = cell.volume
            self.plot_win.add_data_point("VolComp", vol, comp)
            
            cell.lambdaVecY = 500
        
        #uncoment for Wall degradetion
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
        
        # adding new nutrients (coment if not want it)
        field = self.field.Nutr
        # field[:,:,:] = 1 #constant nutrients
        field[0,:,:] = 1 #adding nutrients coming for x = 0 plane
        
        
        
        #saving data as a txt in CSV format
        self.plot_win.save_plot_as_data("plots.txt",CSV_FORMAT)
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)
        
    def start(self):
        #creating the new information of cells
        for cell in self.cell_list_by_type(self.CELL):
            cell.dict["uptake"] = 0
            cell.dict["complexity"] = 0

    def step(self, mcs):          
        #make cells uptake
        secretor = self.get_field_secretor("Nutr")
        for cell in self.cell_list_by_type(self.CELL):
            rat= 2-np.exp(-cell.dict["complexity"]) #more complex cells uptake more nutrients
            # arguments are: cell, max uptake, relative uptake
            # Um = secretor.uptakeInsideCellTotalCount(cell, 0.05*rat, 0.2)
            Um = secretor.uptakeOutsideCellAtBoundaryTotalCount(cell, 0.05*rat, 1)
            
            
            cell.dict["uptake"] += np.abs(Um.tot_amount)
            #make cells grow in volume or complexity when having enough nutrients saved
            if cell.dict["uptake"]>0.1:
                gr_co = np.random.randint(0,2)
                if gr_co == 0:                    
                    cell.targetVolume += 0.5*cell.dict["uptake"]
                    cell.dict["uptake"] = 0
                elif gr_co == 1:
                    cell.dict["complexity"] += cell.dict["uptake"]
                    cell.dict["uptake"] = 0
            

        
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
        #dividing complexity as mitosis happen since organuls will split into parent and child
        self.parent_cell.dict["complexity"] /= 2.0
        self.child_cell.dict["complexity"] /= 2.0

        
