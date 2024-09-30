import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valve0_dp', 'valve1_dp', 'tank1_level', 'der_tank1_level', 'valve0_flow', 'valve1_flow', 'tank1_inflow', 'tank1_outflow', 'der_tank1_V', 'pump_flow'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve0_dp_nominal', 'valve1_Flow_Nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations for flows and derivatives
    -pump_flow + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * sym.sqrt(1 - (valve0_dp / valve0_dp_nominal)**2) * (1 - f_valve0),
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * sym.sqrt(1 - (valve1_dp / valve1_dp_nominal)**2) * (1 - f_valve1),
    -der_tank1_level + (valve0_flow - valve1_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2)**2),
    -der_tank1_V + tank1_inflow - tank1_outflow,
    
    # Equations for measured variables
    -FI_1 + pump_flow,
    -FI_2 + valve0_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_flow,
    
    # Differential constraints
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    fdt.DiffConstraint('der_tank1_V', 'tank1_inflow')  # Assuming tank1_inflow is the variable that changes over time
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur in any of the mentioned lists, add them under key 'x'
# Since 'pump_flow' was not in the original 'x' list, it has been added to the 'x' list in the model definition