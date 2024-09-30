import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['der_tank1_level', 'tank1_level', 'valve0_flow', 'valve1_flow', 'pump_flow'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_N_Nominal', 'pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 
                   'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Pump equation
model_def['rels'] = [
    -pump_flow + pump_N / pump_N_Nominal * pump_V * (1 - f_pumpSlow),
]

# Valve equations
model_def['rels'] += [
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
]

# Tank mass balance
model_def['rels'] += [
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_flow - valve1_flow) / ((tank1_Diameter / 2) ** 2 * 3.14159) - f_tank1leak,
]

# Sensor equations
model_def['rels'] += [
    -FI1 + pump_flow,
    -FI2 + valve0_flow,
    -LI3 + tank1_level,
    -FI4 + valve1_flow,
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur in any of the mentioned lists, add them under key 'x'
additional_variables = ['valve0_dp', 'valve1_dp']
for var in additional_variables:
    if var not in model_def['x'] + model_def['f'] + model_def['z'] + model_def['parameters']:
        model_def['x'].append(var)

# Now the model is ready to be used with the faultdiagnosis toolbox.