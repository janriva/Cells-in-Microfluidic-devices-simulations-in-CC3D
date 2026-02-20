
from cc3d import CompuCellSetup
        

from ProvesCanviCellsSteppables import ProvesCanviCellsSteppable

CompuCellSetup.register_steppable(steppable=ProvesCanviCellsSteppable(frequency=1))


CompuCellSetup.run()
