import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_Q', 'valve0_Q', 'valve1_Q', 'der_tank1_level'],  # unknown variables
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],  # faults
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],  # known variables
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'tank1_Diameter']  # parameters
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations
    -pump_Q + pump_N * pump_V - f_pumpSlow,
    -valve0_Q + valve0_opening * valve0_Flow_Nominal - f_valve0,
    -valve1_Q + valve1_opening * valve1_Flow_Nominal - f_valve1,
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -(der_tank1_level - (valve0_Q - valve1_Q) / (sym.pi * (tank1_Diameter / 2) ** 2) + f_tank1leak),
    
    # Sensor equations
    -FI_1 + pump_Q,
    -FI_2 + valve0_Q,
    -LI_3 + der_tank1_level,
    -FI_4 + valve1_Q
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur in any of the mentioned lists, add them under key 'x'
# In this case, 'tank1_level' is not in any of the lists, so we add it to 'x'
model_def['x'].append('tank1_level')