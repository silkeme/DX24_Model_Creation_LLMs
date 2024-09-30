import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'valve0_flow', 'tank1_level', 'der_tank1_level', 'valve1_flow', 'valve1_V_flow'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations for the pump
    -pump_flow + pump_N * pump_V * (1 - f_pumpSlow),
    
    # Equations for valve0
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    
    # Equations for tank1
    -der_tank1_level + (valve0_flow - valve1_V_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    -tank1_level + LI3,
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    
    # Equations for valve1
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    
    # Assuming valve1 flow is equal to the outflow from tank1
    -valve1_V_flow + valve1_flow,
    
    # Sensor equations
    -FI1 + pump_flow,
    -FI2 + valve0_flow,
    -LI3 + tank1_level,
    -FI4 + valve1_V_flow
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_variables = ['pump_N', 'valve0_opening', 'valve1_opening', 'pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'tank1_Diameter']
for var in additional_variables:
    if var not in model_def['x'] + model_def['f'] + model_def['z'] + model_def['parameters']:
        model_def['x'].append(var)