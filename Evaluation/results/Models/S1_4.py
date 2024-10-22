import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_dp_pump', 'tank1_ports_1__p', 'tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['pump_N', 'valve0_opening', 'valve1_opening', 'FI_1', 'FI_2', 'LI_3', 'FI_4'],
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations for the flows and level derivative
    -pump_flow + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (pump_dp_pump / valve0_dp_nominal)**0.5 * (1 - f_valve0),
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (tank1_ports_1__p / valve1_dp_nominal)**0.5 * (1 - f_valve1),
    -der_tank1_level + (valve0_flow - valve1_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2)**2),
    
    # Equations for the measurements
    -FI_1 + pump_flow,
    -FI_2 + valve0_flow,
    -LI_3 + tank1_ports_1__p,
    -FI_4 + valve1_flow,
    
    # Differential equation for tank1_level
    fdt.DiffConstraint('der_tank1_level', 'tank1_level')
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur in any of the mentioned lists, add them under key 'x'
additional_variables = ['pump_flow', 'valve0_flow', 'valve1_flow', 'der_tank1_level']
for var in additional_variables:
    if var not in model_def['x'] + model_def['f'] + model_def['z'] + model_def['parameters']:
        model_def['x'].append(var)

# Now the model is ready to be used with the faultdiagnosis toolbox.