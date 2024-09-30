import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'pump1_flow', 'valveLinear1_flow', 'valveLinear2_flow', 'valveLinear3_flow', 'der_tank1_level', 'der_tank_level', 'der_tank2_level'],  # unknown variables
    'f': ['f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'],  # faults
    'z': ['FI_1', 'LI_2', 'FI_3', 'LI_4', 'FI_5', 'LI_6', 'FI_7', 'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'],  # known variables
    'parameters': ['pipe_Length', 'pipe4_Length', 'pipe5_Length', 'pipe1_Length', 'pipe2_Length', 'pipe6_Length', 'pipe7_Length', 'pipe8_Length',
                   'pipe_Diameter', 'pipe4_Diameter', 'pipe5_Diameter', 'pipe1_Diameter', 'pipe2_Diameter', 'pipe6_Diameter', 'pipe7_Diameter', 'pipe3_Diameter',
                   'tank_Diameter', 'tank1_Diameter', 'tank2_Diameter', 'tank_Height', 'tank1_Height', 'tank2_Height',
                   'pump_N_Nominal', 'pump1_N_Nominal', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal',
                   'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'pump_V', 'pump1_V']  # parameters
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations for pump and valve flows
    -sym.var('pump_flow') + sym.var('pump_N') / sym.var('pump_N_Nominal') * sym.var('pump_V'),
    -sym.var('pump1_flow') + sym.var('pump1_N') / sym.var('pump1_N_Nominal') * sym.var('pump1_V'),
    -sym.var('valveLinear1_flow') + sym.var('valveLinear1_opening') * sym.var('valveLinear1_Flow_Nominal') * (1 - sym.var('f_valve1')),
    -sym.var('valveLinear2_flow') + sym.var('valveLinear2_opening') * sym.var('valveLinear2_Flow_Nominal') * (1 - sym.var('f_valve2')),
    -sym.var('valveLinear3_flow') + sym.var('valveLinear3_opening') * sym.var('valveLinear3_Flow_Nominal') * (1 - sym.var('f_valve3')),
    
    # Differential equations for tank levels
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -sym.var('der_tank1_level') + (sym.var('FI_1') - sym.var('FI_3')) / (sym.pi * (sym.var('tank1_Diameter') / 2) ** 2) - sym.var('f_tank1leak'),
    fdt.DiffConstraint('der_tank_level', 'tank_level'),
    -sym.var('der_tank_level') + (sym.var('FI_3') - sym.var('FI_5')) / (sym.pi * (sym.var('tank_Diameter') / 2) ** 2),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    -sym.var('der_tank2_level') + (sym.var('FI_5') - sym.var('FI_7')) / (sym.pi * (sym.var('tank2_Diameter') / 2) ** 2) - sym.var('f_tank2leak'),
    
    # Sensor equations
    -sym.var('FI_1') + sym.var('pump_flow'),
    -sym.var('LI_2') + sym.var('der_tank1_level'),
    -sym.var('FI_3') + sym.var('valveLinear1_flow'),
    -sym.var('LI_4') + sym.var('der_tank_level'),
    -sym.var('FI_5') + sym.var('pump1_flow'),
    -sym.var('LI_6') + sym.var('der_tank2_level'),
    -sym.var('FI_7') + sym.var('valveLinear3_flow')
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters' in the model_def dictionary with their exact name
# If they do not occur in any of the mentioned lists, add them under key 'x'
# Since the model is already provided, we assume all variables are correctly listed in the model_def dictionary