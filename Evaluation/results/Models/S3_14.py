import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'tank1_level', 'tank2_level', 'tank3_level', 'tank4_level',
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
        'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow',
        'valveLinear7_V_flow'
    ],
    'f': [
        'f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'
    ],
    'z': [
        'FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17',
        'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening',
        'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening',
        'valveLinear7_opening'
    ],
    'parameters': [
        'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter',
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal',
        'valveLinear3_Flow_Nominal', 'valveLinear4_Flow_Nominal',
        'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal',
        'valveLinear7_Flow_Nominal', 'valveLinear1_dp_nominal',
        'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal',
        'valveLinear4_dp_nominal', 'valveLinear5_dp_nominal',
        'valveLinear6_dp_nominal', 'valveLinear7_dp_nominal'
    ],
    'rels': []
}

# Define the variables
sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Tank level dynamics (continuity equation)
model_def['rels'].append(-der_tank1_level + (valveLinear1_V_flow - valveLinear2_V_flow - valveLinear3_V_flow) / (sym.pi * (tank1_Diameter / 2) ** 2))
model_def['rels'].append(-der_tank2_level + (valveLinear2_V_flow - valveLinear4_V_flow) / (sym.pi * (tank2_Diameter / 2) ** 2) - f_tank2leak)
model_def['rels'].append(-der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / (sym.pi * (tank3_Diameter / 2) ** 2))
model_def['rels'].append(-der_tank4_level + (valveLinear4_V_flow + valveLinear5_V_flow - valveLinear6_V_flow) / (sym.pi * (tank4_Diameter / 2) ** 2) - f_pipe4)

# Valve flow dynamics (assuming linear valve characteristics)
model_def['rels'].append(-valveLinear1_V_flow + valveLinear1_Flow_Nominal * valveLinear1_opening)
model_def['rels'].append(-valveLinear2_V_flow + valveLinear2_Flow_Nominal * valveLinear2_opening)
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_Flow_Nominal * valveLinear3_opening * (1 - f_valve3))
model_def['rels'].append(-valveLinear4_V_flow + valveLinear4_Flow_Nominal * valveLinear4_opening)
model_def['rels'].append(-valveLinear5_V_flow + valveLinear5_Flow_Nominal * valveLinear5_opening)
model_def['rels'].append(-valveLinear6_V_flow + valveLinear6_Flow_Nominal * valveLinear6_opening * (1 - f_valve6))
model_def['rels'].append(-valveLinear7_V_flow + valveLinear7_Flow_Nominal * valveLinear7_opening)

# Sensor equations
model_def['rels'].append(-FI_13 + valveLinear1_V_flow)
model_def['rels'].append(-LI_21 + tank1_level)
model_def['rels'].append(-FI_14 + valveLinear2_V_flow)
model_def['rels'].append(-LI_22 + tank2_level)
model_def['rels'].append(-FI_15 + valveLinear3_V_flow)
model_def['rels'].append(-LI_23 + tank3_level)
model_def['rels'].append(-FI_16 + valveLinear4_V_flow)
model_def['rels'].append(-LI_24 + tank4_level)
model_def['rels'].append(-FI_17 + valveLinear6_V_flow)

# Add differential constraints
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank3_level', 'tank3_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank4_level', 'tank4_level'))

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_vars = ['tank1_level', 'tank2_level', 'tank3_level', 'tank4_level']
for var in additional_vars:
    if var not in model_def['x']:
        model_def['x'].append(var)

# Now the model is ready to be used with the faultdiagnosis toolbox