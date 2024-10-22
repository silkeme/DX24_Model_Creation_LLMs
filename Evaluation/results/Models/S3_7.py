import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level',
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
        'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow',
        'tank1_Area', 'tank2_Area', 'tank3_Area', 'tank4_Area'  # Added tank areas to 'x'
    ],
    'f': [
        'f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'
    ],
    'z': [
        'FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17',
        'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening',
        'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'
    ],
    'parameters': [
        'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter',
        'tank1_Height', 'tank2_Height', 'tank3_Height', 'tank4_Height',
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal',
        'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal'
    ],
    'rels': []
}

# Create symbolic variables
sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Store the equations in the model definition
model_def['rels'] += [
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal,
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal,
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal,
    -valveLinear4_V_flow + valveLinear4_opening * valveLinear4_Flow_Nominal,
    -valveLinear5_V_flow + valveLinear5_opening * valveLinear5_Flow_Nominal,
    -valveLinear6_V_flow + valveLinear6_opening * valveLinear6_Flow_Nominal,
    -tank1_Area + (tank1_Diameter / 2) ** 2 * 3.14159,
    -tank2_Area + (tank2_Diameter / 2) ** 2 * 3.14159,
    -tank3_Area + (tank3_Diameter / 2) ** 2 * 3.14159,
    -tank4_Area + (tank4_Diameter / 2) ** 2 * 3.14159,
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / tank1_Area,
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    -der_tank2_level + (valveLinear2_V_flow - valveLinear4_V_flow) / tank2_Area - f_tank2leak,
    fdt.DiffConstraint('der_tank3_level', 'tank3_level'),
    -der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / tank3_Area,
    fdt.DiffConstraint('der_tank4_level', 'tank4_level'),
    -der_tank4_level + (valveLinear4_V_flow + valveLinear5_V_flow - valveLinear6_V_flow) / tank4_Area,
    -FI_13 + valveLinear1_V_flow,
    -LI_21 + der_tank1_level * tank1_Area,
    -FI_14 + valveLinear2_V_flow,
    -LI_22 + der_tank2_level * tank2_Area,
    -FI_15 + valveLinear3_V_flow * (1 - f_valve3),
    -LI_23 + der_tank3_level * tank3_Area,
    -FI_16 + valveLinear4_V_flow * (1 - f_pipe4),
    -LI_24 + der_tank4_level * tank4_Area,
    -FI_17 + valveLinear6_V_flow * (1 - f_valve6)
]

# Add missing variables to 'x' if they are not already in 'x', 'f', 'z', or 'parameters'
missing_vars = ['tank1_level', 'tank2_level', 'tank3_level', 'tank4_level']
for var in missing_vars:
    if var not in model_def['x'] and var not in model_def['f'] and var not in model_def['z'] and var not in model_def['parameters']:
        model_def['x'].append(var)

# Now the model is ready to be used with the faultdiagnosistoolbox