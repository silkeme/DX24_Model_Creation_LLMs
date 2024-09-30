import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'valve0_flow', 'valve1_flow', 'der_tank1_level', 'tank1_level'], 
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'], 
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'], 
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Process equations
    -pump_flow + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_flow - valve1_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    
    # Sensor equations
    -FI1 + pump_flow,
    -FI2 + valve0_flow,
    -LI3 + tank1_level,
    -FI4 + valve1_flow
]