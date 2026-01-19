from cc3d.core.PySteppables import *
import numpy as np



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)
        
        self.tgVl=10.         # liquid target volume 
        self.lbdVl=100.         # liquid lambda volume
        self.Fxl=-300

    def start(self):

        for cell in self.cell_list_by_type(self.CELL):

            cell.targetVolume = 120
            cell.lambdaVolume = 10.00
            
        for cell in self.cell_list_by_type(self.LIQUID):
            cell.targetVolume = self.tgVl
            cell.lambdaVolume = self.lbdVl
            cell.lambdaVecX = self.Fxl
            cell.dict["oldXcm"]=cell.xCOM       # dict entry for old cell x CM
            cell.dict["oldYcm"]=cell.yCOM       # dict entry for old cell y CM
        
           
        firstWall = None
        for cell in self.cell_list_by_type(self.WALL):
            if firstWall:
                self.merge_cells(cell, firstWall)
                print(cell.id,firstWall.id)
            else:
                firstWall = cell
                print(cell.id,firstWall.id)
        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)
        self.tgVl=10.         # liquid target volume 
        self.lbdVl=100.         # liquid lambda volume
        self.Fxl=-300
        
        self.vectorField = self.create_vector_field_cell_level_py("VELOCITY")
        self.scalarField = self.create_scalar_field_cell_level_py("PRESSURE")
        self.scalarField2 = self.create_scalar_field_py("AVGPRESSURE")
    def start(self):    
        self.pAvg = np.zeros((self.dim.x,self.dim.y))
        self.pAvgStartMCS = np.zeros((self.dim.x,self.dim.y))

    def step(self, mcs):
        for cell in self.cell_list_by_type(self.CELL):
            cell.targetVolume += 0.1        

        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        # field = self.field.CHEMICAL_FIELD_NAME
        
        # for cell in self.cell_list:
            # concentrationAtCOM = field[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]

            # # you can use here any fcn of concentrationAtCOM
            # cell.targetVolume += 0.01 * concentrationAtCOM       
        timeinterval = 10      # time interval between cell events (source/sink)
        if mcs%timeinterval == 0:
            x = 5                   # cell source x position
            for y in range(2+1,self.dim.y-3,2):
                # cell source y position
                currentCell = self.cell_field[x, y, 0]  # attributes the lattice point to a temp cell
                if (not currentCell):    # ift that point belongs to MEDUM...
                    self.cell_field[x,y, 0] = self.new_cell(self.LIQUID)  # creates a NEW cell at it,...
                    newCell = self.cell_field[x,y,0]   # and say that the point belongs to the NEW cell
                    newCell.targetVolume=self.tgVl     # give the the attributes
                    newCell.lambdaVolume=self.lbdVl
                    newCell.lambdaVecX=self.Fxl
                    newCell.dict["oldXcm"]=x
                    newCell.dict["oldYcm"]=y

            
            # if the cell reaches the sink, delete it
            for cell in self.cell_list_by_type(self.LIQUID):
                if cell.xCOM > 480:      # if the cell X cm crosses xSink position...
                    self.delete_cell(cell) 
                    
            for cell in self.cell_list_by_type(self.CELL):
                if cell.xCOM > 480:      # if the cell X cm crosses xSink position...
                    self.delete_cell(cell) 
                    
                elif cell.targetVolume-cell.volume>10: #Mort per pressió
                    self.delete_cell(cell)
                    
            fieldV = self.vectorField                        # placeholder for the vector field
            fieldS = self.scalarField                        # placeholder for the scalar field
            for cell in self.cell_list_by_type(self.LIQUID):
                delX=cell.xCOM-cell.dict["oldXcm"]                   # cell x displacement
                if   delX<-self.dim.x/2.: delX+=self.dim.x           # x periodic bounday correction
                elif delX> self.dim.x/2.: delX-=self.dim.x 
                CVelX=delX/timeinterval                                  # cell x compon Vel
                #
                delY=cell.yCOM-cell.dict["oldYcm"]                    # cell y displacement
                if   delY<-self.dim.y/2.: delY+=self.dim.y          # y periodic bounday correction
                elif delY> self.dim.y/2.: delY-=self.dim.y 
                CVelY=delY/timeinterval                                 # cell y compon Vel

                fieldV[cell] = [CVelX, CVelY, 0.]                        # filling the field with values
                #fieldS[cell] = cell.pressure                        # filling the field with values
                fieldS[cell] = cell.targetVolume - cell.volume       # filling the field with values
               
                cell.dict["oldXcm"]=cell.xCOM                           # storing actual cell x CM
                cell.dict["oldYcm"]=cell.yCOM                           # storing actual cell x CM
            for cell in self.cell_list_by_type(self.CELL):
                fieldS[cell] = cell.targetVolume - cell.volume
                cell.dict["oldXcm"]=cell.xCOM                           
                cell.dict["oldYcm"]=cell.yCOM
                
    # updating the Average Pressure field
            if mcs > 0:
                fieldAvgPress = self.scalarField2      # placeholder for the pixel-based scalar field
                for x, y, z in self.every_pixel():
                    if x > 10 and x < 480:  # don't calculate average pressure to close to the cell source
                        cell = self.cell_field[x,y,z]
                        if cell:  # skip this pixel if it is Medium
                            if self.pAvgStartMCS[x,y] == 0:  # don't start averaging for a pixel until it is part of a cell
                                self.pAvgStartMCS[x,y] = mcs - timeinterval
                            cellPress = cell.targetVolume - cell.volume
                            #oldSum = self.pAvg[x,y]*(mcs-timeinterval)/float(timeinterval)
                            oldSum = self.pAvg[x,y]*(mcs-self.pAvgStartMCS[x,y]-timeinterval)/float(timeinterval)
                            newSum = oldSum + cellPress
                            #newAvg = newSum/float(mcs)/timeinterval)
                            newAvg = newSum/float((mcs-self.pAvgStartMCS[x,y])/timeinterval)
                            self.pAvg[x,y] = newAvg
                            #print(mcs,timeinterval,mcs/timeinterval,"   ",self.pAvg[x,y],oldSum,cellPress,newSum,newAvg)
                            fieldAvgPress[x,y,z]=newAvg
                    #print('\t\t\t max and min average pixel pressure:',np.amax(self.pAvg),np.amin(self.pAvg))
     
        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.CELL):
            if cell.volume>100:
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
        
        if self.parent_cell.type==1:
            self.child_cell.type=1
        else:
            self.child_cell.type=1

        