import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'tank1_level', 'der_tank1_level'],  # unknown variables
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],  # faults
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],  # known variables
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'tank1_Diameter']  # parameters
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Pump flow equation with fault
    -pump_V_flow + pump_N * pump_V * (1 - f_pumpSlow),
    # Valve0 flow equation with fault
    -valve0_V_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    # Valve1 flow equation with fault
    -valve1_V_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    # Tank level equation with fault
    -der_tank1_level + (valve0_V_flow - valve1_V_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    # Sensor equations
    -FI_1 + pump_V_flow,
    -FI_2 + valve0_V_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_V_flow
]

# Adding differential constraint for tank level
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))

# Output the complete model
print(model_def)