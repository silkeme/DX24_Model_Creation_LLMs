import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'valve0_dp', 'valve0_flow', 'valve1_dp', 'valve1_flow', 'tank1_level', 'der_tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve0_dp_nominal', 'valve1_Flow_Nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Process equations
    -pump_flow + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - (valve0_dp / valve0_dp_nominal)**2)**0.5 * (1 - f_valve0),
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - (valve1_dp / valve1_dp_nominal)**2)**0.5 * (1 - f_valve1),
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_flow - valve1_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2)**2),
    
    # Sensor equations
    -FI_1 + pump_flow,
    -FI_2 + valve0_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_flow
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_variables = ['pump_N', 'valve0_opening', 'valve1_opening']
for var in additional_variables:
    if var not in model_def['x'] + model_def['f'] + model_def['z'] + model_def['parameters']:
        model_def['x'].append(var)