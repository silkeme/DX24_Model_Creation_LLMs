import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow', 'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow', 'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level'],
    'f': ['f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'],
    'z': ['FI13', 'LI21', 'FI14', 'LI22', 'FI15', 'LI23', 'FI16', 'LI24', 'FI17', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening', 'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'],
    'parameters': ['tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Valve flow equations
    -valveLinear1_V_flow + valveLinear1_Flow_Nominal * valveLinear1_opening,
    -valveLinear2_V_flow + valveLinear2_Flow_Nominal * valveLinear2_opening * (1 - f_valve3),
    -valveLinear3_V_flow + valveLinear3_Flow_Nominal * valveLinear3_opening,
    -valveLinear4_V_flow + valveLinear4_Flow_Nominal * valveLinear4_opening * (1 - f_pipe4),
    -valveLinear5_V_flow + valveLinear5_Flow_Nominal * valveLinear5_opening,
    -valveLinear6_V_flow + valveLinear6_Flow_Nominal * valveLinear6_opening * (1 - f_valve6),
    
    # Tank cross-sectional area equations
    -tank1_cross_sectional_area + (tank1_Diameter / 2) ** 2 * 3.14159,
    -tank2_cross_sectional_area + (tank2_Diameter / 2) ** 2 * 3.14159,
    -tank3_cross_sectional_area + (tank3_Diameter / 2) ** 2 * 3.14159,
    -tank4_cross_sectional_area + (tank4_Diameter / 2) ** 2 * 3.14159,
    
    # Tank level derivative equations
    -der_tank1_level + (FI13 - valveLinear2_V_flow - valveLinear3_V_flow) / tank1_cross_sectional_area,
    -der_tank2_level + (valveLinear2_V_flow - valveLinear4_V_flow) / tank2_cross_sectional_area - f_tank2leak,
    -der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / tank3_cross_sectional_area,
    -der_tank4_level + (valveLinear4_V_flow + valveLinear5_V_flow - FI17) / tank4_cross_sectional_area,
    
    # Sensor equations
    -FI13 + valveLinear1_V_flow,
    -LI21 + der_tank1_level,
    -FI14 + valveLinear2_V_flow,
    -LI22 + der_tank2_level,
    -FI15 + valveLinear3_V_flow,
    -LI23 + der_tank3_level,
    -FI16 + valveLinear4_V_flow,
    -LI24 + der_tank4_level,
    -FI17 + valveLinear6_V_flow,
    
    # Differential equations
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    fdt.DiffConstraint('der_tank3_level', 'tank3_level'),
    fdt.DiffConstraint('der_tank4_level', 'tank4_level')
]

# Add missing variables to 'x' if they are not already there
additional_vars = ['tank1_level', 'tank2_level', 'tank3_level', 'tank4_level', 'tank1_cross_sectional_area', 'tank2_cross_sectional_area', 'tank3_cross_sectional_area', 'tank4_cross_sectional_area']
for var in additional_vars:
    if var not in model_def['x']:
        model_def['x'].append(var)