# Nozzle.py
# Created: Anil Variyar, Jul 2014
# Modified: Trent Lukaczyk, Aug 2014


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

from Component import Component
import numpy as np

# ----------------------------------------------------------------------
#   Nozzle
# ----------------------------------------------------------------------

class Nozzle(Component):
    """ a nozzle component
    """    
    
    def __defaults__(self):
        
        self.tag = 'Nozzle'

        self.etapold = 1.0
        self.pid = 1.0
        
        self.inputs.Tt=0.
        self.inputs.Pt=0.
        
        self.outputs.Tt=0.
        self.outputs.Pt=0.
        self.outputs.ht=0.

        return

        
    def compute(self,conditions):
        
        #unpack the variables
        gamma = conditions.freestream.gamma
        Cp    = conditions.freestream.Cp
        Po    = conditions.freestream.pressure
        
        Tt_in = self.inputs.Tt
        Pt_in = self.inputs.Pt

    
        
        #Computing the output modules
        
        #--Getting the outptu stagnation quantities
        Pt_out=Pt_in*self.pid
        Tt_out=Tt_in*self.pid**((gamma-1)/(gamma*self.etapold))
        ht_out=Cp*Tt_out 
        
        
        #compute the output Mach number, static quantities and the output velocity
        Mach=np.sqrt((((Pt_out/Po)**((gamma-1)/gamma))-1)*2/(gamma-1))
        T_out=Tt_out/(1+(gamma-1)/2*Mach**2)
        h_out=Cp*T_out
        u_out=np.sqrt(2*(ht_out-h_out))  
        
        #pack outputs
        self.outputs.Tt=Tt_out
        self.outputs.Pt=Pt_out
        self.outputs.ht=ht_out
        self.outputs.M = Mach
        self.outputs.T = T_out
        self.outputs.h = h_out
        self.outputs.u = u_out
        
        return
        
    
    __call__ = compute