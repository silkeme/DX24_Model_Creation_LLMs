import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow_rate', 'valve0_flow_rate', 'valve1_flow_rate', 'der_tank1_level'],  # unknown variables
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],  # faults
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],  # known variables
    'parameters': ['tank1_Diameter', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'pump_V']  # parameters
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Process equations
    -pump_flow_rate + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_flow_rate + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    -valve1_flow_rate + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_flow_rate - valve1_flow_rate - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    
    # Sensor equations
    -FI1 + pump_flow_rate,
    -FI2 + valve0_flow_rate,
    -LI3 + der_tank1_level,
    -FI4 + valve1_flow_rate
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_vars = ['tank1_level']
model_def['x'].extend(additional_vars)