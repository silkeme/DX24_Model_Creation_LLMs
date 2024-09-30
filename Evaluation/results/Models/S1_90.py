import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valve0_dp', 'valve1_dp', 'der_tank1_level', 'pump_flow', 'valve0_flow', 'valve1_flow', 'tank1_level'],  # unknown variables
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],  # faults
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],  # known variables
    'parameters': ['pump_N_Nominal', 'pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']  # parameters
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Sensor equations
    -FI1 + pump_flow,
    -FI2 + valve0_flow,
    -LI3 + tank1_level,
    -FI4 + valve1_flow,
    
    # Pump equation with fault
    -pump_flow + (pump_N / pump_N_Nominal * pump_V) * (1 - f_pumpSlow),
    
    # Valve equations with faults
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - valve0_dp / valve0_dp_nominal) * (1 - f_valve0),
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - valve1_dp / valve1_dp_nominal) * (1 - f_valve1),
    
    # Tank level equation with fault
    -der_tank1_level + (valve0_flow - valve1_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    -tank1_level + LI3
]

# Adding differential constraint for the tank level derivative
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))