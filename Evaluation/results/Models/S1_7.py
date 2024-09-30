import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_Q', 'valve0_Q', 'valve1_Q', 'der_tank1_level', 'tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['tank1_Diameter', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'pump_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Process equations
    -pump_Q + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_Q + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    -valve1_Q + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_Q - valve1_Q - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    
    # Sensor equations
    -FI_1 + pump_Q,
    -FI_2 + valve0_Q,
    -LI_3 + tank1_level,
    -FI_4 + valve1_Q
]