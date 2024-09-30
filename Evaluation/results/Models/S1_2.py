import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'valve0_flow', 'valve0_dp', 'der_tank1_level', 'valve1_flow', 'valve1_dp'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Process equations
    -pump_flow + pump_N * pump_V - f_pumpSlow,
    -valve0_flow + valve0_opening * valve0_Flow_Nominal - f_valve0,
    -valve0_dp + valve0_flow ** 2 * valve0_dp_nominal,
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -(der_tank1_level - (valve0_flow - valve1_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2)),
    -valve1_flow + valve1_opening * valve1_Flow_Nominal - f_valve1,
    -valve1_dp + valve1_flow ** 2 * valve1_dp_nominal,
    
    # Sensor equations
    -FI_1 + pump_flow,
    -FI_2 + valve0_flow,
    -LI_3 + der_tank1_level,
    -FI_4 + valve1_flow
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_variables = ['tank1_level']
model_def['x'].extend(additional_variables)