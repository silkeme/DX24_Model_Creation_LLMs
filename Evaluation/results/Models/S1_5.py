import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_Q', 'valve0_Q', 'valve1_Q', 'der_tank1_level', 'tank1_level'], 
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'], 
    'z': ['FI_1', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'], 
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'tank1_Diameter'],
    'rels': []
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Sensor equations
model_def['rels'].append(-FI_1 + pump_Q)
model_def['rels'].append(-LI_3 + tank1_level)
model_def['rels'].append(-FI_4 + valve1_Q)

# Component equations with faults
model_def['rels'].append(-pump_Q + (pump_N * pump_V) * (1 - f_pumpSlow))
model_def['rels'].append(-valve0_Q + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0))
model_def['rels'].append(-valve1_Q + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1))
model_def['rels'].append(-der_tank1_level + ((valve0_Q - valve1_Q) / (tank1_Diameter**2 * sym.pi / 4)) - f_tank1leak)

# Adding differential constraints
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))