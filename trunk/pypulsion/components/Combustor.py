# Nozzle.py
# Created: Anil Variyar, Jul 2014
# Modified: Trent Lukaczyk, Aug 2014


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

from Component import Component


# ----------------------------------------------------------------------
#   Combustor
# ----------------------------------------------------------------------
    
class Combustor(Component):
    """ a combustor component
    """    
    
    def __defaults__(self):

        self.tag = 'Combustor'
        
        self.eta = 1.0
        self.tau = 1.0
        self.To = 273.0
        self.alphac = 0.0 
        self.Tt4 = 1.0
        
        self.fuel_specific_energy = 41.0
        
        self.inputs.Tt = 1.0
        self.inputs.Pt = 1.0  
        self.inputs.nozzle_temp = 1.0     
        
        self.outputs.Tt=1.0
        self.outputs.Pt=1.0
        self.outputs.ht=1.0
        self.outputs.f = 1.0        
        
        
    def compute(self,conditions):
        
        #unpack the variables
        gamma=conditions.freestream.gamma
        Cp = conditions.freestream.Cp
        To = conditions.freestream.temperature
        
        Tt_in = self.inputs.Tt 
        Pt_in = self.inputs.Pt   
        Tt_n = self.inputs.nozzle_temp 
        Tto = self.inputs.freestream_stag_temp
        
        htf=self.fuel_specific_energy
        ht4 = Cp*self.Tt4
        ho = Cp*To
        
        # Using the Turbine exit temperature, the fuel properties and 
        # freestream temperature to compute the fuel to air ratio f        
        tau = htf/(Cp*To)
        tau_freestream=Tto/To
            
        f = (ht4 - ho)/(htf-ht4)
        
        ht_out=Cp*self.Tt4
        Pt_out=Pt_in*self.pib  
        
        #pack outputs
        self.outputs.Tt=self.Tt4
        self.outputs.Pt=Pt_out
        self.outputs.ht=ht_out 
        self.outputs.f = f
        
        return
        
    __call__ = compute
   