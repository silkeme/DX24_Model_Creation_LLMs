import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['tank1_level', 'tank2_level', 'tank3_level', 'tank4_level', 'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level', 'valveLinear1_dp', 'valveLinear2_dp', 'valveLinear3_dp', 'valveLinear4_dp', 'valveLinear5_dp', 'valveLinear6_dp', 'valveLinear7_dp'],
    'f': ['f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'],
    'z': ['FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening', 'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening', 'valveLinear7_opening'],
    'parameters': ['tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal', 'valveLinear7_Flow_Nominal', 'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'valveLinear4_dp_nominal', 'valveLinear5_dp_nominal', 'valveLinear6_dp_nominal', 'valveLinear7_dp_nominal']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Valve flow equations
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * sym.sqrt(1 - (valveLinear1_dp / valveLinear1_dp_nominal)**2),
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * sym.sqrt(1 - (valveLinear2_dp / valveLinear2_dp_nominal)**2),
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * sym.sqrt(1 - (valveLinear3_dp / valveLinear3_dp_nominal)**2) * (1 - f_valve3),
    -valveLinear4_V_flow + valveLinear4_opening * valveLinear4_Flow_Nominal * sym.sqrt(1 - (valveLinear4_dp / valveLinear4_dp_nominal)**2) * (1 - f_pipe4),
    -valveLinear5_V_flow + valveLinear5_opening * valveLinear5_Flow_Nominal * sym.sqrt(1 - (valveLinear5_dp / valveLinear5_dp_nominal)**2),
    -valveLinear6_V_flow + valveLinear6_opening * valveLinear6_Flow_Nominal * sym.sqrt(1 - (valveLinear6_dp / valveLinear6_dp_nominal)**2) * (1 - f_valve6),
    -valveLinear7_V_flow + valveLinear7_opening * valveLinear7_Flow_Nominal * sym.sqrt(1 - (valveLinear7_dp / valveLinear7_dp_nominal)**2),
    
    # Tank level equations
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / (sym.pi * (tank1_Diameter / 2)**2),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    -der_tank2_level + (valveLinear2_V_flow - valveLinear4_V_flow) / (sym.pi * (tank2_Diameter / 2)**2) - f_tank2leak,
    fdt.DiffConstraint('der_tank3_level', 'tank3_level'),
    -der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / (sym.pi * (tank3_Diameter / 2)**2),
    fdt.DiffConstraint('der_tank4_level', 'tank4_level'),
    -der_tank4_level + (valveLinear4_V_flow + valveLinear5_V_flow - valveLinear6_V_flow) / (sym.pi * (tank4_Diameter / 2)**2),
    
    # Sensor equations
    -FI_13 + valveLinear1_V_flow,
    -LI_21 + tank1_level,
    -FI_14 + valveLinear2_V_flow,
    -LI_22 + tank2_level,
    -FI_15 + valveLinear3_V_flow,
    -LI_23 + tank3_level,
    -FI_16 + valveLinear4_V_flow,
    -LI_24 + tank4_level,
    -FI_17 + valveLinear6_V_flow
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_vars = ['valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow', 'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow', 'valveLinear7_V_flow', 'tank1_cross_sectional_area', 'tank2_cross_sectional_area', 'tank3_cross_sectional_area', 'tank4_cross_sectional_area']
for var in additional_vars:
    if var not in model_def['x'] and var not in model_def['f'] and var not in model_def['z'] and var not in model_def['parameters']:
        model_def['x'].append(var)