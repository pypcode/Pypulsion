# Component.py
# Created: Trent Lukaczyk, Aug 2014

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from pypulsion.structure import Data
from pypulsion.structure import Container as ContainerBase


# ----------------------------------------------------------------------
#  Component
# ----------------------------------------------------------------------

class Component(Data):
    """ pypulsion.components.Component()
        the base component class
    """
    def __defaults__(self):
        self.tag    = 'Component'
        self.origin = [0.0,0.0,0.0]
        self.inputs = Data()
        self.outputs = Data()
    
    
# ----------------------------------------------------------------------
#  Component Container
# ----------------------------------------------------------------------

class Container(ContainerBase):
    """ SUAVE.Components.Component.Container()
        the base component container class
    """
    pass


# ------------------------------------------------------------
#  Handle Linking
# ------------------------------------------------------------

Component.Container = Container