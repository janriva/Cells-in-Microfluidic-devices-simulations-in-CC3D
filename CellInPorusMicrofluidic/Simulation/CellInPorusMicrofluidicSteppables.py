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
        circleRadius= 50
        N_porus = 20
        dim = self.dim.x
        #probability distribution parameters
        pics = 3
        sig = 1
        
        #creating the probability distribution (PD)
        dist_prob=np.zeros(dim)
        for pp in range(pics):
            # dist_prob += np.sinc(2*np.pi*(np.arange(0,dim)-pp*dim/pics))
                        
            dist_prob += np.exp(-(np.arange(0, dim)-(pp+1/2)*dim/pics)**2/(2*sig**2))
            
        dist_prob[:5] = 0
        dist_prob[-5:]=0
        dist_prob = dist_prob/dist_prob.sum()
        #Selecting the porus positions based on PD
        pos_cent_x = np.random.choice(self.dim.x,size=N_porus, p = dist_prob, replace=False)
        pos_cent_y = np.random.choice(self.dim.y,size=N_porus, p = dist_prob, replace=False)
        
        
        #If we want uniform distribution use next:
        # pos_cent_x = np.random.randint(0,self.dim.x, size = N_porus)
        # pos_cent_y = np.random.randint(0,self.dim.y, size = N_porus)

        
        newCell = self.new_cell(self.WALL)
        #porus generation with cells in center
        for nn1 in range(N_porus):
            #adding the cells at the center
            newCell2 = self.new_cell(self.CELL)
            centx = int(pos_cent_x[nn1])
            centy = int(pos_cent_y[nn1])
            self.cell_field[centx-6:centx+6, centy-6:centy+6,:] = newCell2
            #create the circle wall (porus)
            for dd in range(wallWidth):
                R = circleRadius+dd
                for ang in np.linspace(0,2*np.pi, 4*(int(R))):
                    dins = False
                    px = int(pos_cent_x[nn1]+R* np.cos(ang))
                    py = int(pos_cent_y[nn1]+R* np.sin(ang))
                    #check if inside a porus and far from edges
                    if (px+2<= self.dim.x-1 and px>=0) and (py+2<=self.dim.y-1 and py>=0):
                        for nn2 in range(N_porus):
                            if nn1!=nn2:
                                if ((px-pos_cent_x[nn2])**2 + (py-pos_cent_y[nn2])**2)<(circleRadius)**2:
                                    dins = True
                                    break
                        #if not inside create the new cell
                        if not(dins):
                            self.cell_field[px:px+2,py:py+2,:] = newCell
        self.cell_field[0,:,:] = newCell
        self.cell_field[self.dim.x-1,:,:] = newCell
        self.cell_field[:,0,:] = newCell
        self.cell_field[:,self.dim.y-1,:] = newCell

        #setting cells parameters
        for cell in self.cell_list_by_type(self.CELL):

            cell.targetVolume = 45
            cell.lambdaVolume = 2.0

        #Creating initial nutrient field
        field = self.field.Nutr
        field[:,:,:]=1 #initial nutrient
        
    def step(self,mcs):

        
        self.plot_win.erase_all_data()
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume < 3:
                self.delete_cell(cell)
                continue

            #saving complexity and volume parameters in plot
            comp = cell.dict["complexity"]
            vol = cell.volume
            # arguments are (name of the data series, x, y)
            self.plot_win.add_data_point("VolComp", vol, comp)
            
            cell.lambdaVecY = 80 #coment to take the force out

        #ensuring constant concentration
        field = self.field.Nutr
        # field[:,:,:] = 1
        # field[:,self.dim.y-1,:]=1
        
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
            #make cells grow randomly in volume or complexity when having enough nutrients saved
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
         #dividing complexity as mitosis happen since organuls will split into parent and child
        self.parent_cell.dict["complexity"] /= 2.0
        self.child_cell.dict["complexity"] /= 2.0
