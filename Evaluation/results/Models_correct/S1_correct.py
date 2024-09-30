import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'der_tank1_level', 'tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['tank1_Diameter', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    -der_tank1_level + (valve0_V_flow - valve1_V_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    -pump_V_flow + valve0_V_flow,
    -valve0_V_flow + valve0_Flow_Nominal * valve0_opening * (1 - f_valve0),
    -valve1_V_flow + valve1_Flow_Nominal * valve1_opening * (1 - f_valve1),
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -FI_1 + pump_V_flow,
    -FI_2 + valve0_V_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_V_flow
]

