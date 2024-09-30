import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'der_tank1_level'],  # unknown variables
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],  # faults
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],  # known variables
    'parameters': [
        'pipe_Diameter', 'pipe4_Diameter', 'tank1_Diameter', 'pipe1_Diameter',
        'pipe2_Diameter', 'pipe_Length', 'pipe4_Length', 'pipe1_Length',
        'pipe2_Length', 'tank1_Height', 'pump_N_Nominal', 'valve0_Flow_Nominal',
        'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'pump_V'
    ]  # parameters
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Equations
model_def['rels'] = [
    # Sensor equations
    -FI_1 + pump_V_flow,
    -FI_2 + valve0_V_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_V_flow,
    
    # Pump flow equation with fault
    -pump_V_flow + pump_N * pump_V * (1 - f_pumpSlow),
    
    # Valve flow equations with faults
    -valve0_V_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    -valve1_V_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    
    # Tank level derivative equation with fault
    -der_tank1_level + (valve0_V_flow - valve1_V_flow) / (tank1_Diameter**2 * sym.pi / 4) - f_tank1leak,
    
    # Differential constraints
    fdt.DiffConstraint('der_tank1_level', 'tank1_level')
]

# Output the complete model
print(model_def)