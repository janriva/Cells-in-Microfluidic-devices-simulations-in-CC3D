
from cc3d import CompuCellSetup
        

from WallDegradetionSteppables import WallDegradetionSteppable

CompuCellSetup.register_steppable(steppable=WallDegradetionSteppable(frequency=1))


CompuCellSetup.run()
