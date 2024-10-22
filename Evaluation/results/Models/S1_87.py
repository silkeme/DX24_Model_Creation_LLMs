import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'der_tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['tank1_Diameter', 'pump_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Process equations
    -pump_V_flow + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_V_flow + valve0_opening * (FI_1 - FI_2) * (1 - f_valve0),
    -valve1_V_flow + valve1_opening * LI_3 * (1 - f_valve1),
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (FI_2 - FI_4 - f_tank1leak) / (tank1_Diameter**2 * sym.pi / 4),
    
    # Sensor equations
    -FI_1 + pump_V_flow,
    -FI_2 + valve0_V_flow,
    -LI_3 + der_tank1_level,
    -FI_4 + valve1_V_flow
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_variables = ['tank1_level']
model_def['x'].extend(additional_variables)