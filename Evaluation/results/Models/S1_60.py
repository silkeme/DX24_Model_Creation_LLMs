import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_Q', 'valve0_Q', 'valve1_Q', 'tank1_level', 'der_tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Sensor equations
    -FI1 + pump_Q,
    -FI2 + valve0_Q,
    -LI3 + tank1_level,
    -FI4 + valve1_Q,
    
    # Component equations with faults
    -pump_Q + (pump_N - f_pumpSlow) * pump_V,
    -valve0_Q + (valve0_opening - f_valve0) * valve0_Flow_Nominal,
    -valve1_Q + (valve1_opening - f_valve1) * valve1_Flow_Nominal,
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_Q - valve1_Q - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2)
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur in any of the mentioned lists, add them under key 'x'
# Since all variables are already listed in the model_def dictionary, no additional variables need to be added.