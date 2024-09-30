import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valve0_dp', 'valve1_dp', 'der_tank1_level', 'tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_N_Nominal', 'pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Pump equation
    -FI1 + pump_N / pump_N_Nominal * pump_V * (1 - f_pumpSlow),
    
    # Valve equations
    -FI2 + valve0_opening * valve0_Flow_Nominal * (1 - valve0_dp / valve0_dp_nominal) * (1 - f_valve0),
    -FI4 + valve1_opening * valve1_Flow_Nominal * (1 - valve1_dp / valve1_dp_nominal) * (1 - f_valve1),
    
    # Tank level equation
    -der_tank1_level + (FI2 - FI4 - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    
    # Sensor equations
    -LI3 + tank1_level,
    
    # Differential equation for tank level
    fdt.DiffConstraint('der_tank1_level', 'tank1_level')
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur in any of the mentioned lists, add them under key 'x'
# In this case, 'tank1_level' was missing from 'x' and has been added