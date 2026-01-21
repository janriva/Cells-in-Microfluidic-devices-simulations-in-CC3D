
from cc3d import CompuCellSetup
        

from Advection_ChemSteppables import Advection_ChemSteppable

CompuCellSetup.register_steppable(steppable=Advection_ChemSteppable(frequency=1))


CompuCellSetup.run()
