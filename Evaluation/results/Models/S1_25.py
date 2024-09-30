import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'valve0_flow', 'der_tank1_level', 'valve1_flow', 'valve1_V_flow', 'tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pipe_Diameter', 'pipe4_Diameter', 'tank1_Diameter', 'pipe1_Diameter', 'pipe2_Diameter', 'pipe_Length', 'pipe4_Length', 'pipe1_Length', 'pipe2_Length', 'tank1_Height', 'pump_N_Nominal', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'pump_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations for the pump
    -pump_flow + pump_N * pump_V * (1 - f_pumpSlow),
    
    # Equations for valve0
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    
    # Equations for tank1
    -der_tank1_level + (valve0_flow - valve1_V_flow) / (sym.pi * (tank1_Diameter / 2) ** 2) - f_tank1leak,
    
    # Equations for valve1
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    
    # Assuming valve1_V_flow is the flow rate through valve1
    -valve1_V_flow + valve1_flow,
    
    # Sensor equations
    -FI1 + pump_flow,
    -FI2 + valve0_flow,
    -LI3 + tank1_level,
    -FI4 + valve1_flow
]

# Adding differential constraints
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))