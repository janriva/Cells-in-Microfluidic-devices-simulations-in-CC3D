from cc3d.cpp.PlayerPython import * 
from cc3d import CompuCellSetup
from cc3d.core.PySteppables import *
import numpy as np



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):
        self.flux = 1
        
        shape = [3,3]
        wallWidth  =  1
        circleRadius= self.dim.x/(max(shape)*2) -2
        holeWidth = 5 #degrees half width
        
        
        newCell = self.new_cell(self.WALL)
        for ii in range(shape[0]):
            nx_circ = shape[0]
            pasx_circ=self.dim.x/(2*nx_circ)
            
            xMid = pasx_circ+2*pasx_circ*ii
            
            for jj in range(shape[1]):
                ny_circ = shape[1]
                pasy_circ=self.dim.y/(2*ny_circ)
            
                yMid = pasy_circ+2*pasy_circ*jj
                
                #ponts en x
                if ii !=0:
                    R = circleRadius
                    if ii == shape[0]-1:
                        px = int(xMid+R* np.cos(holeWidth*(np.pi/180)))
                        py = int(yMid+R* np.sin(holeWidth*(np.pi/180)))
                        self.cell_field[px:,py:py+2,:] = newCell
                    
                        px = int(xMid+R* np.cos(2*np.pi -holeWidth*(np.pi/180)))
                        py = int(yMid+R* np.sin(2*np.pi -holeWidth*(np.pi/180)))
                        self.cell_field[px:,py:py+2,:] = newCell
                    else:    
                        px = int(xMid+R* np.cos(holeWidth*(np.pi/180)))
                        py = int(yMid+R* np.sin(holeWidth*(np.pi/180)))
                        self.cell_field[px:pasx_circ+2*pasx_circ*(ii+1)-R,py:py+2,:] = newCell
                    
                        px = int(xMid+R* np.cos(2*np.pi -holeWidth*(np.pi/180)))
                        py = int(yMid+R* np.sin(2*np.pi -holeWidth*(np.pi/180)))
                        self.cell_field[px:pasx_circ+2*pasx_circ*(ii+1)-R,py:py+2,:] = newCell
                    
                    px = int(xMid+R* np.cos(np.pi -holeWidth*(np.pi/180)))
                    py = int(yMid+R* np.sin(np.pi -holeWidth*(np.pi/180)))
                    self.cell_field[pasx_circ+2*pasx_circ*(ii-1)+R:px,py:py+2,:] = newCell
                    px = int(xMid+R* np.cos(np.pi +holeWidth*(np.pi/180)))
                    py = int(yMid+R* np.sin(np.pi +holeWidth*(np.pi/180)))
                    self.cell_field[pasx_circ+2*pasx_circ*(ii-1)+R:px,py:py+2,:] = newCell
                    
                else:
                    R = circleRadius
                    px = int(xMid+R* np.cos(np.pi -holeWidth*(np.pi/180)))
                    py = int(yMid+R* np.sin(np.pi -holeWidth*(np.pi/180)))
                    self.cell_field[:px,py:py+2,:] = newCell
                    
                    px = int(xMid+R* np.cos(np.pi +holeWidth*(np.pi/180)))
                    py = int(yMid+R* np.sin(np.pi +holeWidth*(np.pi/180)))
                    self.cell_field[:px,py:py+2,:] = newCell
                    
                #ponts en y    
                if jj !=0:
                    R = circleRadius
                    if jj == shape[1]-1:
                        px = int(xMid+R* np.cos(np.pi/2 -holeWidth*(np.pi/180)))
                        py = int(yMid+R* np.sin(np.pi/2 -holeWidth*(np.pi/180)))
                        self.cell_field[px:px+2,py:,:] = newCell
                    
                        px = int(xMid+R* np.cos(np.pi/2 +holeWidth*(np.pi/180)))
                        py = int(yMid+R* np.sin(np.pi/2 +holeWidth*(np.pi/180)))
                        self.cell_field[px:px+2,py:,:] = newCell
                    else:    
                        px = int(xMid+R* np.cos(np.pi/2 -holeWidth*(np.pi/180)))
                        py = int(yMid+R* np.sin(np.pi/2 -holeWidth*(np.pi/180)))
                        self.cell_field[px:px+2,py:pasy_circ+2*pasy_circ*(jj+1)-R,:] = newCell
                    
                        px = int(xMid+R* np.cos(np.pi/2 +holeWidth*(np.pi/180)))
                        py = int(yMid+R* np.sin(np.pi/2 +holeWidth*(np.pi/180)))
                        self.cell_field[px:px+2,py:pasy_circ+2*pasy_circ*(jj+1)-R,:] = newCell
                    
                    px = int(xMid+R* np.cos(3*np.pi/2 -holeWidth*(np.pi/180)))
                    py = int(yMid+R* np.sin(3*np.pi/2 -holeWidth*(np.pi/180)))
                    self.cell_field[px:px+2,pasy_circ+2*pasy_circ*(jj-1)+R:py,:] = newCell
                    px = int(xMid+R* np.cos(3*np.pi/2 +holeWidth*(np.pi/180)))
                    py = int(yMid+R* np.sin(3*np.pi/2 +holeWidth*(np.pi/180)))
                    self.cell_field[px:px+2,pasy_circ+2*pasy_circ*(jj-1)+R:py,:] = newCell
                    
                else:
                    R = circleRadius
                    px = int(xMid+R* np.cos(3*np.pi/2 -holeWidth*(np.pi/180)))
                    py = int(yMid+R* np.sin(3*np.pi/2 -holeWidth*(np.pi/180)))
                    self.cell_field[px:px+2,:py,:] = newCell
                    
                    px = int(xMid+R* np.cos(3*np.pi/2 +holeWidth*(np.pi/180)))
                    py = int(yMid+R* np.sin(3*np.pi/2 +holeWidth*(np.pi/180)))
                    self.cell_field[px:px+2,:py,:] = newCell
        
                for dd in range(wallWidth):
                    R = circleRadius +dd
                    
                    for ang in np.linspace(0,2*np.pi,4*(int(R))):
                        if ang<holeWidth*(np.pi/180) or ang>2*np.pi -holeWidth*(np.pi/180):
                            continue
                        elif ang>np.pi -holeWidth*(np.pi/180) and ang<np.pi +holeWidth*(np.pi/180):
                            continue
                            
                        elif ang>np.pi/2 -holeWidth*(np.pi/180) and ang<np.pi/2 +holeWidth*(np.pi/180):
                            continue
                        elif ang>3*np.pi/2 -holeWidth*(np.pi/180) and ang<3*np.pi/2 +holeWidth*(np.pi/180):
                            continue
                            
                        px = int(xMid+R* np.cos(ang))
                        py = int(yMid+R* np.sin(ang))
                        
                        self.cell_field[px:px+2,py:py+2,:] = newCell
        
        for cell in self.cell_list_by_type(self.CELL):

            cell.targetVolume = 8
            cell.lambdaVolume = 4.0
            
        field = self.field.OXYGEN
        field[30:40,30:40,:]=1 #aliment inicial
        self.old_field=field
        
        self.v= []
        l_h = 2*circleRadius*np.cos(np.pi/2-holeWidth*np.pi/180)
        self.v_0 = 1*self.flux
        for j in range(self.dim.y):
            for jj in range(shape[1]):
                if j<pasy_circ+2*pasy_circ*jj+circleRadius:
                    pos_ny = jj
                    break
                else:
                    pos_ny = 0
            pos = j-2*pasy_circ*pos_ny-pasy_circ
            #esta en un canal?
            if pos<circleRadius and pos>-circleRadius:
                l = 2*np.sqrt(circleRadius**2-pos**2)
            else:
                l = l_h
            
            self.v.append(self.v_0*l_h/l)
        
        #alternativa calc v
        camp_cell = self.cell_field
        
        arr_cell = np.zeros((self.dim.x,self.dim.y))
        
        for jj in range(self.dim.y):
            for ii in range(self.dim.x):
                cell =  camp_cell[ii,jj,0]
                if cell:
                    if cell.type == 1:
                        arr_cell[ii,jj] = 1
                    else:
                        arr_cell[ii,jj] = 0
                else:
                    arr_cell[ii,jj] = 0
                if ii == 0 or ii == self.dim.x -1 or jj==0 or jj == self.dim.y-1:
                    arr_cell[ii,jj] = 1
                
        self.camp_v = self.create_scalar_field_py("Velocity")

        for ii in range(self.dim.x):
            for jj in range(self.dim.y):
                if camp_cell[ii,jj,0]:
                    self.camp_v[ii,jj,:] = 0
                    continue
                if ii == 0:
                    pos_esq = 0
                    pos_dret = np.argmax(arr_cell[ii:,jj])
                elif ii == self.dim.x -1:
                    pos_esq = np.argmax(np.flip(arr_cell[:ii,jj]))
                    pos_dret = 0
                else:
                    pos_dret = np.argmax(arr_cell[ii:,jj])
                    pos_esq = np.argmax(np.flip(arr_cell[:ii,jj]))
                
                l = pos_dret+pos_esq
                if l !=0 and l>=l_h:
                    self.camp_v[ii,jj,:] = self.v_0*l_h/l
                else:
                    self.camp_v[ii,jj,:] = self.v_0   
                    
    def step(self,mcs):
        shape = [3,3]
        wallWidth  =  1
        circleRadius= self.dim.x/(max(shape)*2) -2
        holeWidth = 5 #degrees half width
        
        pasy_circ=self.dim.y/(2*shape[1])
        for cell in self.cell_list_by_type(self.CELL):
            for jj in range(shape[1]):
                if cell.yCOM<pasy_circ+2*pasy_circ*jj+circleRadius:
                    pos_ny = jj
                    break
                else:
                    pos_ny = 0
            pos_celly = cell.yCOM-2*pasy_circ*pos_ny-pasy_circ
            #esta en un canal?
            if pos_celly<circleRadius and pos_celly>-circleRadius:
                l = 2*np.sqrt(circleRadius**2-pos_celly**2)
            else:
                l = 2*circleRadius*np.cos(np.pi/2-holeWidth*np.pi/180)
            
            cell.lambdaVecY = -circleRadius/l * 10 *self.flux
            
        
        
        field = self.field.OXYGEN
        field[:, 0, :] = 1*np.sin(mcs/100)**2
        # field[148:152, 0, :] = 1*np.sin(mcs/100)**2
        
        for i, j, k in self.every_pixel():
            cell = self.cell_field[i,j,k]
            if cell:
                if cell.type==1:#Avoiding errors with the solver making sure the wall doesn't take O2
                    field[i, j, k] = 0
            else:
                if j!= 0 and j!=self.dim.y-1:
                    # dC = -(self.v[j+1]*self.old_field[i, j+1, k]-self.v[j-1]*self.old_field[i, j-1, k])
                    dC = -(self.camp_v[i,j+1,k]*self.old_field[i, j+1, k]-self.camp_v[i,j-1,k]*self.old_field[i, j-1, k])
                    field[i,j,k] += np.float64(dC)
                elif j==0:
                    dC = -self.v_0*(self.old_field[i, j+1, k]-self.old_field[i, 99, k])
                    field[i,j,k] += dC
                elif j==self.dim.y-1:
                    dC = -self.v_0*(self.old_field[i, 0, k]-self.old_field[i, j-1, k])
                    field[i,j,k] += dC
        self.old_field = field
                        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)
        
    def start(self):
        for cell in self.cell_list_by_type(self.CELL):
            cell.dict["uptake"] = 0

    def step(self, mcs):
        secretor = self.get_field_secretor("OXYGEN")
        for cell in self.cell_list_by_type(self.CELL):     
            # arguments are: cell, max uptake, relative uptake
            Um = secretor.uptakeInsideCellTotalCount(cell, 0.2, 0.02)
            cell.dict["uptake"] = np.abs(Um.tot_amount)
            cell.targetVolume += 1*cell.dict["uptake"]

        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        field = self.field.OXYGEN
        
        # for cell in self.cell_list:
            # concentrationAtCOM = field[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]

            # you can use here any fcn of concentrationAtCOM
            # cell.targetVolume += 0.1 * concentrationAtCOM       

        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)
        

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume>15:
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
       

        