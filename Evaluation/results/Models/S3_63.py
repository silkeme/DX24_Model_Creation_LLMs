import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow', 'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow', 'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level'],
    'f': ['f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'],
    'z': ['FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening', 'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'],
    'parameters': ['tank1_cross_sectional_area', 'tank2_cross_sectional_area', 'tank3_cross_sectional_area', 'tank4_cross_sectional_area', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal', 'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Valve flow equations
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal,
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal,
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3),
    -valveLinear4_V_flow + valveLinear4_opening * valveLinear4_Flow_Nominal * (1 - f_pipe4),
    -valveLinear5_V_flow + valveLinear5_opening * valveLinear5_Flow_Nominal,
    -valveLinear6_V_flow + valveLinear6_opening * valveLinear6_Flow_Nominal * (1 - f_valve6),
    
    # Tank cross-sectional area equations
    -tank1_cross_sectional_area + (tank1_Diameter / 2) ** 2 * 3.14159,
    -tank2_cross_sectional_area + (tank2_Diameter / 2) ** 2 * 3.14159,
    -tank3_cross_sectional_area + (tank3_Diameter / 2) ** 2 * 3.14159,
    -tank4_cross_sectional_area + (tank4_Diameter / 2) ** 2 * 3.14159,
    
    # Tank level derivative equations
    -der_tank1_level + (FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / tank1_cross_sectional_area,
    -der_tank2_level + (valveLinear2_V_flow - FI_16 - f_tank2leak) / tank2_cross_sectional_area,
    -der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / tank3_cross_sectional_area,
    -der_tank4_level + (FI_16 + valveLinear5_V_flow - FI_17) / tank4_cross_sectional_area,
    
    # Sensor equations
    -FI_13 + valveLinear1_V_flow,
    -LI_21 + der_tank1_level,
    -FI_14 + valveLinear2_V_flow,
    -LI_22 + der_tank2_level,
    -FI_15 + valveLinear3_V_flow,
    -LI_23 + der_tank3_level,
    -FI_16 + valveLinear4_V_flow,
    -LI_24 + der_tank4_level,
    -FI_17 + valveLinear6_V_flow
]

# Adding differential constraints
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank3_level', 'tank3_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank4_level', 'tank4_level'))

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_variables = ['tank1_level', 'tank2_level', 'tank3_level', 'tank4_level']
for var in additional_variables:
    if var not in model_def['x']:
        model_def['x'].append(var)