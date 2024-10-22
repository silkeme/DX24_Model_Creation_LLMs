import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'valve0_flow', 'valve0_dp', 'tank1_level', 'valve1_flow', 'valve1_dp'],  # unknown variables
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],  # faults
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],  # known variables
    'parameters': ['pipe_Diameter', 'pipe4_Diameter', 'tank1_Diameter', 'pipe1_Diameter',
                   'pipe2_Diameter', 'pipe_Length', 'pipe4_Length', 'pipe1_Length',
                   'pipe2_Length', 'tank1_Height', 'pump_N_Nominal', 'valve0_Flow_Nominal',
                   'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'pump_V']  # parameters
}

# Define the variables as sympy symbols
sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Equations
model_def['rels'] = [
    # Sensor equations
    -FI_1 + pump_flow,
    -FI_2 + valve0_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_flow,
    
    # Pump flow equation with fault
    -pump_flow + pump_N * pump_V * (1 - f_pumpSlow),
    
    # Valve0 flow equation with fault
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - (valve0_dp / valve0_dp_nominal)**2) * (1 - f_valve0),
    
    # Valve1 flow equation with fault
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - (valve1_dp / valve1_dp_nominal)**2) * (1 - f_valve1),
    
    # Differential equation for tank1 level with fault
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_flow - valve1_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2)**2),
    
    # Valve pressure drop equations
    -valve0_dp + valve0_flow**2 / valve0_Flow_Nominal,
    -valve1_dp + valve1_flow**2 / valve1_Flow_Nominal
]

# Output the complete model
print(model_def)