# Nozzle.py
# Created: Anil Varyar, Jul 2014
# Modified: Trent Lukaczyk, Aug 2014


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

from Component import Component


# ----------------------------------------------------------------------
#   Nozzle
# ----------------------------------------------------------------------

class Turbine(Component):
    """ a Turbine component
    """    
    
    def __defaults__(self):
        
        self.tag ='Turbine'
        
        self.eta_mech =1.0
        self.Cp =1004
        self.gamma =1.4
        self.etapolt = 1.0
        
        self.inputs.Tt = 1.0
        self.inputs.Pt = 1.0  
        self.inputs.h_compressor_out = 1.0
        self.inputs.h_compressor_in = 1.0
        self.inputs.f = 1.0
        
        self.outputs.Tt=1.0
        self.outputs.Pt=1.0
        self.outputs.ht=1.0    
        
        return
     
        
    def compute(self,conditions):
        
        #unpack inputs
        gamma=conditions.freestream.gamma
        Cp = conditions.freestream.Cp 
        
        Tt_in =self.inputs.Tt 
        Pt_in =self.inputs.Pt   
        h_compressor_out =self.inputs.h_compressor_out 
        h_compressor_in=self.inputs.h_compressor_in
        h_fan_out =  self.inputs.h_fan_out
        h_fan_in = self.inputs.h_fan_in
        alpha =  self.inputs.alpha
        f =self.inputs.f        
        
        # Using the stagnation enthalpy drop across the corresponding
        # turbine and the fuel to air ratio to compute the energy drop across the turbine
        deltah_ht = -1/(1+f)*1/self.eta_mech*\
                   ((h_compressor_out-h_compressor_in)+ alpha*(h_fan_out-h_fan_in))
        
        # Compute the output stagnation quantities from the inputs 
        # and the energy drop computed above 
        Tt_out=Tt_in+deltah_ht/Cp
        Pt_out=Pt_in*(Tt_out/Tt_in)**(gamma/((gamma-1)*self.etapolt))
        ht_out=Cp*Tt_out 
        
        #pack outputs
        self.outputs.Tt=Tt_out
        self.outputs.Pt=Pt_out
        self.outputs.ht=ht_out        
        
        return
        
    __call__ = compute      
    