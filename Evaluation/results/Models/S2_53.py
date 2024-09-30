import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['der_tank1_level', 'der_tank2_level', 'der_tank_level', 'pump_flow', 'pump1_flow', 'tank_level', 'tank1_level', 'tank2_level', 'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow'],
    'f': ['f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'],
    'z': ['FI_1', 'LI_2', 'FI_3', 'LI_4', 'FI_5', 'LI_6', 'FI_7', 'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'],
    'parameters': ['pipe_Length', 'pipe4_Length', 'pipe5_Length', 'pipe1_Length', 'pipe2_Length', 'pipe6_Length', 'pipe7_Length', 'pipe8_Length', 'pipe_Diameter', 'pipe4_Diameter', 'pipe5_Diameter', 'pipe1_Diameter', 'pipe2_Diameter', 'pipe6_Diameter', 'pipe7_Diameter', 'pipe3_Diameter', 'tank_Height', 'tank1_Height', 'tank2_Height', 'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'pump_N_Nominal', 'pump1_N_Nominal', 'pump_V', 'pump1_V', 'tank1_Diameter', 'tank2_Diameter', 'tank_Diameter', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations for pumps
    -pump_flow + pump_N / pump_N_Nominal * pump_V,
    -pump1_flow + pump1_N / pump1_N_Nominal * pump1_V,
    
    # Equations for tanks
    -der_tank1_level + (pump_flow - valveLinear1_V_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    -der_tank2_level + (pump_flow - valveLinear3_V_flow - f_tank2leak) / (sym.pi * (tank2_Diameter / 2) ** 2),
    -der_tank_level + (valveLinear1_V_flow - pump1_flow) / (sym.pi * (tank_Diameter / 2) ** 2),
    
    # Equations for valves
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1),
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (1 - f_valve2),
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3),
    
    # Sensor equations
    -FI_1 + pump_flow,
    -LI_2 + tank1_level,
    -FI_3 + valveLinear1_V_flow,
    -LI_4 + tank_level,
    -FI_5 + pump1_flow,
    -LI_6 + tank2_level,
    -FI_7 + valveLinear3_V_flow,
    
    # Differential equations
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    fdt.DiffConstraint('der_tank_level', 'tank_level')
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur, add them under key 'x'
# Additional variables identified from the equations that are not in the lists
additional_vars = ['pump_N_Nominal', 'pump1_N_Nominal', 'pump_V', 'pump1_V', 'tank1_Diameter', 'tank2_Diameter', 'tank_Diameter', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal']
for var in additional_vars:
    if var not in model_def['x'] and var not in model_def['f'] and var not in model_def['z'] and var not in model_def['parameters']:
        model_def['x'].append(var)