# Nozzle.py
# Created: Anil Variyar, Jul 2014
# Modified: Trent Lukaczyk, Aug 2014


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

from Component import Component


# ----------------------------------------------------------------------
#   Compressor
# ----------------------------------------------------------------------

class Compressor(Component):
    """ a compressor component
    """    
    
    def __defaults__(self):

        self.tag = 'Compressor'

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
        gamma=conditions.freestream.gamma
        Cp = conditions.freestream.Cp  
        Tt_in = self.inputs.Tt
        Pt_in = self.inputs.Pt        
    
        #Compute the output stagnation quantities based on the pressure ratio of the component
        Pt_out=Pt_in*self.pid
        Tt_out=Tt_in*self.pid**((gamma-1)/(gamma*self.etapold))
        ht_out=Cp*Tt_out 
        
        #pack outputs
        self.outputs.Tt=Tt_out
        self.outputs.Pt=Pt_out
        self.outputs.ht=ht_out  
        
        return
        
    __call__ = compute