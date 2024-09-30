import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'tank1_level', 'valve0_dp', 'valve1_dp', 'der_tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Sensor equations
    -FI1 + pump_V_flow,
    -FI2 + valve0_V_flow,
    -LI3 + tank1_level,
    -FI4 + valve1_V_flow,
    
    # Pump flow equation
    -pump_V_flow + pump_N * pump_V * (1 - f_pumpSlow),
    
    # Valve flow equations
    -valve0_V_flow + valve0_opening * valve0_Flow_Nominal * (1 - (valve0_dp / valve0_dp_nominal)) * (1 - f_valve0),
    -valve1_V_flow + valve1_opening * valve1_Flow_Nominal * (1 - (valve1_dp / valve1_dp_nominal)) * (1 - f_valve1),
    
    # Tank level equation (differential equation)
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_V_flow - valve1_V_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    
    # Valve pressure drop equations
    -valve0_dp + valve0_V_flow ** 2,
    -valve1_dp + valve1_V_flow ** 2
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters' in the model_def dictionary
# If not, add them under key 'x'
additional_vars = ['pump_N', 'pump_V', 'valve0_opening', 'valve1_opening', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
for var in additional_vars:
    if var not in model_def['x'] + model_def['f'] + model_def['z'] + model_def['parameters']:
        model_def['x'].append(var)