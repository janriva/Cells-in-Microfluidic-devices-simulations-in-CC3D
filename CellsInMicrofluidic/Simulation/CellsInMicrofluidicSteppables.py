from cc3d.core.PySteppables import *
import numpy as np



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):
        shape = [2,2]
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

            cell.targetVolume = 10
            cell.lambdaVolume = 4.0
            
        field = self.field.OXYGEN
        self.old_field=field
        
        self.v= []
        l_h = 2*circleRadius*np.cos(np.pi/2-holeWidth*np.pi/180)
        self.v_0 = 0.5
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
            
    def step(self,mcs):
        shape = [2,2]
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
            
            cell.lambdaVecY = -circleRadius/l * 50
            
        
        
        field = self.field.OXYGEN
        # v = 0.1
        dt = 1
        dx = 1
        field[24:27, 0, :] = 1*np.sin(mcs/100)**2
        field[74:77, 0, :] = 1*np.sin(mcs/100)**2
        # field[74:77, 20, :] = 1
        
        for i, j, k in self.every_pixel():
            cell = self.cell_field[i,j,k]
            if cell:
                if cell.type==1:#Avoiding errors with the solver making sure the wall doesn't take O2
                    field[i, j, k] = 0
            else:
                if j!= 0 and j!=99:
                    dC = -(self.v[j+1]*self.old_field[i, j+1, k]-self.v[j-1]*self.old_field[i, j-1, k])*(dt/dx)
                    field[i,j,k] += dC
                elif i==0:
                    dC = -self.v_0*(self.old_field[i, j+1, k]-self.old_field[i, 99, k])*(dt/dx)
                    field[i,j,k] += dC
                elif i==99:
                    dC = -self.v_0*(self.old_field[i, 0, k]-self.old_field[i, j-1, k])*(dt/dx)
                    field[i,j,k] += dC
        self.old_field = field
                        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        # for cell in self.cell_list_by_type(self.CELL):
            # cell.targetVolume += 0.1

        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        field = self.field.OXYGEN
        
        for cell in self.cell_list:
            concentrationAtCOM = field[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]

            # you can use here any fcn of concentrationAtCOM
            cell.targetVolume += 0.1 * concentrationAtCOM       

        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume>20:
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
       

        