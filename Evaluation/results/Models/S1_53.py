import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'tank1_level', 'der_tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_N_Nominal', 'pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    -pump_V_flow + pump_N / pump_N_Nominal * pump_V * (1 - f_pumpSlow),
    -valve0_V_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    -valve1_V_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    -der_tank1_level + (valve0_V_flow - valve1_V_flow - f_tank1leak) / ((3.14159265359 * tank1_Diameter**2) / 4),
    -FI1 + pump_V_flow,
    -FI2 + valve0_V_flow,
    -LI3 + tank1_level,
    -FI4 + valve1_V_flow
]

# Adding the differential constraint for the level of the tank
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
# In this case, all variables are already included in the lists