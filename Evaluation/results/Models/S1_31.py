import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'der_tank1_level', 'tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_V', 'tank1_Diameter', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Define additional variables that are not in the lists
sym.var('A_tank1')

# Sensor equations
model_def['rels'] = [
    -FI_1 + pump_V_flow,
    -FI_2 + valve0_V_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_V_flow,
    
    # Pump equation
    -pump_V_flow + pump_N * pump_V * (1 - f_pumpSlow),
    
    # Valve equations
    -valve0_V_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    -valve1_V_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    
    # Tank level equation
    -A_tank1 + 3.14159 * (tank1_Diameter / 2)**2,
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_V_flow - valve1_V_flow - f_tank1leak) / A_tank1
]