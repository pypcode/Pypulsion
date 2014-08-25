# test_1
# Written: Anil Variyar, Jul 2014
# Modified: Trent Lukaczyk, Aug 2014
     
# ------------------------------------------------------------------
#   Imports
# ------------------------------------------------------------------

import pypulsion
from pypulsion.structure import Data


# ------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------

def main():
    
    # ------------------------------------------------------------------
    #   Conditions
    # ------------------------------------------------------------------
    
    # setup conditions
    conditions = Data()
    conditions.frames       = Data()
    conditions.freestream   = Data()
    conditions.aerodynamics = Data()
    conditions.propulsion   = Data()
    conditions.weights      = Data()
    conditions.energies     = Data()

    # freestream conditions
    conditions.freestream.velocity       = 223.
    conditions.freestream.mach_number    = 0.8
    conditions.freestream.pressure       = 20000.
    conditions.freestream.temperature    = 215.
    conditions.freestream.density        = 0.8
    conditions.freestream.speed_of_sound = 300.
    conditions.freestream.viscosity      = 0.000001
    conditions.freestream.altitude       = 10.
    conditions.freestream.gravity        = 9.8
    conditions.freestream.gamma          = 1.4
    conditions.freestream.total_temperature = 200.
    conditions.freestream.total_pressure = 1.e6
    conditions.freestream.Cp             = 1.0

    # propulsion conditions
    conditions.propulsion.throttle       =  1.0


    # ------------------------------------------------------------------
    #   Components
    # ------------------------------------------------------------------
    
    # inlet nozzle
    inlet_nozzle = pypulsion.components.Nozzle()
    inlet_nozzle.tag = 'inlet nozzle'
    inlet_nozzle.etapold = 1.0
    inlet_nozzle.pid = 1.0
 
    # low pressure compressor    
    low_pressure_compressor = pypulsion.components.Compressor()
    low_pressure_compressor.tag = 'lpc'
    low_pressure_compressor.etapold = 0.94
    low_pressure_compressor.pid = 1.14
      
    # high pressure compressor  
    high_pressure_compressor = pypulsion.components.Compressor()
    high_pressure_compressor.tag = 'hpc'
    high_pressure_compressor.etapold = 0.91
    high_pressure_compressor.pid = 13.2
    
    # combustor  
    combustor = pypulsion.components.Combustor()
    combustor.tag = 'Comb'
    combustor.eta = 0.95
    combustor.alphac = 1.0     
    combustor.Tt4 =   1400
    combustor.pib =   0.99
    combustor.fuel_specific_energy = 43.02e6 
    
    # low pressure turbine  
    low_pressure_turbine = pypulsion.components.Turbine()
    low_pressure_turbine.tag='lpt'
    low_pressure_turbine.eta_mech =0.99
    low_pressure_turbine.etapolt = 0.87       
    
    # high pressure turbine  
    high_pressure_turbine = pypulsion.components.Turbine()
    high_pressure_turbine.tag='hpt'
    high_pressure_turbine.eta_mech =0.99
    high_pressure_turbine.etapolt = 0.91       
    
    
    # ------------------------------------------------------------------
    #   Nozzle 
    # ------------------------------------------------------------------
    
    inlet_nozzle.inputs.Tt = conditions.freestream.total_temperature
    inlet_nozzle.inputs.Pt = conditions.freestream.total_pressure
    
    inlet_nozzle.compute(conditions)   
    
    # ------------------------------------------------------------------
    #   Low Pressure Compressor
    # ------------------------------------------------------------------
    
    low_pressure_compressor.inputs.Tt = inlet_nozzle.outputs.Tt
    low_pressure_compressor.inputs.Pt = inlet_nozzle.outputs.Pt
    
    low_pressure_compressor.compute(conditions) 
    
    
    # ------------------------------------------------------------------
    #   High Pressure Compressor
    # ------------------------------------------------------------------
    
    high_pressure_compressor.inputs.Tt = low_pressure_compressor.outputs.Tt
    high_pressure_compressor.inputs.Pt = low_pressure_compressor.outputs.Pt        
    
    high_pressure_compressor.compute(conditions) 


    # ------------------------------------------------------------------
    #   Combustor
    # ------------------------------------------------------------------    
    
    combustor.inputs.Tt = high_pressure_compressor.outputs.Tt
    combustor.inputs.Pt = high_pressure_compressor.outputs.Pt   
    combustor.inputs.nozzle_temp = inlet_nozzle.outputs.Tt
    combustor.inputs.freestream_stag_temp = conditions.freestream.stagnation_temperature
    
    combustor.compute(conditions)
    
    
    # ------------------------------------------------------------------
    #   High Pressure Turbine
    # ------------------------------------------------------------------    
    
    high_pressure_turbine.inputs.Tt = combustor.outputs.Tt
    high_pressure_turbine.inputs.Pt = combustor.outputs.Pt    
    high_pressure_turbine.inputs.h_compressor_out = high_pressure_compressor.outputs.ht
    high_pressure_turbine.inputs.h_compressor_in = low_pressure_compressor.outputs.ht
    high_pressure_turbine.inputs.f = combustor.outputs.f
    high_pressure_turbine.inputs.h_fan_out =  0.0
    high_pressure_turbine.inputs.h_fan_in = 0.0
    high_pressure_turbine.inputs.alpha =0.0    
    
    self.high_pressure_turbine.compute(conditions)
    
    
    # ------------------------------------------------------------------
    #   Low Pressure Turbine
    # ------------------------------------------------------------------    
    
    low_pressure_turbine.inputs.Tt = high_pressure_turbine.outputs.Tt
    low_pressure_turbine.inputs.Pt = high_pressure_turbine.outputs.Pt    
    low_pressure_turbine.inputs.h_compressor_out = low_pressure_compressor.outputs.ht
    low_pressure_turbine.inputs.h_compressor_in = inlet_nozzle.outputs.ht
    low_pressure_turbine.inputs.f = combustor.outputs.f   
    
    self.low_pressure_turbine(conditions)
    
        
# ------------------------------------------------------------------
#   Call Main
# ------------------------------------------------------------------    
if __name__ == '__main__':
    main()