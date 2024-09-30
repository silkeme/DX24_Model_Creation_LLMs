import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'valve0_dp', 'valve1_dp', 'tank1_level', 'der_tank1_level', 'tank1_Area'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['tank1_Diameter', 'pump_N_Nominal', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'pump_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Sensor equations
    -FI_1 + pump_V_flow,
    -FI_2 + valve0_V_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_V_flow,
    
    # Pump equation with fault
    -pump_V_flow + (pump_N / pump_N_Nominal * pump_V) * (1 - f_pumpSlow),
    
    # Valve equations with faults
    -valve0_V_flow + valve0_opening * valve0_Flow_Nominal * (valve0_dp / valve0_dp_nominal) * (1 - f_valve0),
    -valve1_V_flow + valve1_opening * valve1_Flow_Nominal * (valve1_dp / valve1_dp_nominal) * (1 - f_valve1),
    
    # Tank level equation with fault
    -tank1_Area + (tank1_Diameter / 2) ** 2 * 3.14159,
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + ((valve0_V_flow - valve1_V_flow) / tank1_Area) - f_tank1leak
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_variables = ['pump_N', 'pump_N_Nominal', 'pump_V', 'valve0_opening', 'valve0_Flow_Nominal', 'valve0_dp_nominal', 'valve1_opening', 'valve1_Flow_Nominal', 'valve1_dp_nominal', 'tank1_Diameter']
for var in additional_variables:
    if var not in model_def['x'] + model_def['f'] + model_def['z'] + model_def['parameters']:
        model_def['x'].append(var)