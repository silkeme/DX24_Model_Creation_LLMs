import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'pump1_flow', 'valveLinear1_flow', 'valveLinear2_flow', 'valveLinear3_flow',
          'der_tank1_level', 'der_tank_level', 'der_tank2_level', 'tank1_level', 'tank_level', 'tank2_level'],
    'f': ['f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'],
    'z': ['FI_1', 'LI_2', 'FI_3', 'LI_4', 'FI_5', 'LI_6', 'FI_7', 'pump_N', 'pump1_N', 'valveLinear1_opening', 
          'valveLinear2_opening', 'valveLinear3_opening'],
    'parameters': ['pipe_Length', 'pipe4_Length', 'pipe5_Length', 'pipe1_Length', 'pipe2_Length', 
                   'pipe6_Length', 'pipe7_Length', 'pipe8_Length', 'pipe_Diameter', 'pipe4_Diameter', 
                   'pipe5_Diameter', 'pipe1_Diameter', 'pipe2_Diameter', 'pipe6_Diameter', 'pipe7_Diameter', 
                   'pipe3_Diameter', 'tank_Diameter', 'tank1_Diameter', 'tank2_Diameter', 'tank_Height', 
                   'tank1_Height', 'tank2_Height', 'pump_N_Nominal', 'pump1_N_Nominal', 
                   'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 
                   'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 
                   'pump_V', 'pump1_V']
}

# Define the variables
sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Define the equations and add them to the model definition
model_def['rels'] = [
    # Flow equations
    -pump_flow + pump_N / pump_N_Nominal * pump_V,
    -pump1_flow + pump1_N / pump1_N_Nominal * pump1_V,
    -valveLinear1_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1),
    -valveLinear2_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (1 - f_valve2),
    -valveLinear3_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3),
    
    # Differential equations for tank levels
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -(der_tank1_level - (pump_flow - valveLinear1_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2)**2)),
    fdt.DiffConstraint('der_tank_level', 'tank_level'),
    -(der_tank_level - (valveLinear1_flow - pump1_flow) / (sym.pi * (tank_Diameter / 2)**2)),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    -(der_tank2_level - (pump1_flow - valveLinear3_flow - f_tank2leak) / (sym.pi * (tank2_Diameter / 2)**2)),
    
    # Sensor equations
    -FI_1 + pump_flow,
    -LI_2 + tank1_level,
    -FI_3 + valveLinear1_flow,
    -LI_4 + tank_level,
    -FI_5 + pump1_flow,
    -LI_6 + tank2_level,
    -FI_7 + valveLinear3_flow
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
# In this case, all variables are already included in the lists, so no additional action is needed.

# Now the model is ready to be used with the faultdiagnosis toolbox