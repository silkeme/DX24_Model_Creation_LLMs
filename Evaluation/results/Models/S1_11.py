import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valve0_dp', 'valve1_dp', 'der_tank1_level', 'valve0_flow', 'valve1_flow', 'pump_flow'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pipe_Diameter', 'pipe4_Diameter', 'tank1_Diameter', 'pipe1_Diameter', 'pipe2_Diameter', 'pipe_Length', 'pipe4_Length', 'pipe1_Length', 'pipe2_Length', 'tank1_Height', 'pump_N_Nominal', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'pump_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Pump equation
    -pump_flow + pump_N / pump_N_Nominal * pump_V * (1 - f_pumpSlow),
    -FI1 + pump_flow,
    
    # Valve equations
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * sym.sqrt(1 - (valve0_dp / valve0_dp_nominal)**2) * (1 - f_valve0),
    -FI2 + valve0_flow,
    
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * sym.sqrt(1 - (valve1_dp / valve1_dp_nominal)**2) * (1 - f_valve1),
    -FI4 + valve1_flow,
    
    # Tank1 mass balance
    -der_tank1_level + (valve0_flow - valve1_flow) / (sym.pi * (tank1_Diameter / 2)**2) - f_tank1leak,
    -LI3 + der_tank1_level
]

# Adding differential constraints
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_variables = ['tank1_level']
for var in additional_variables:
    if var not in model_def['x']:
        model_def['x'].append(var)