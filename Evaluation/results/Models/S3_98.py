import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valveLinear1_dp', 'valveLinear2_dp', 'valveLinear3_dp', 'valveLinear4_dp', 'valveLinear5_dp',
          'valveLinear6_dp', 'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level'],
    'f': ['f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'],
    'z': [FI_13, LI_21, FI_14, LI_22, FI_15, LI_23, FI_16, LI_24, FI_17,
          'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening',
          'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'],
    'parameters': ['valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal',
                   'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal',
                   'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal',
                   'valveLinear4_dp_nominal', 'valveLinear5_dp_nominal', 'valveLinear6_dp_nominal',
                   'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Valve flow equations
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * (valveLinear1_dp / valveLinear1_dp_nominal)**0.5,
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (valveLinear2_dp / valveLinear2_dp_nominal)**0.5,
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (valveLinear3_dp / valveLinear3_dp_nominal)**0.5 * (1 - f_valve3),
    -valveLinear4_V_flow + valveLinear4_opening * valveLinear4_Flow_Nominal * (valveLinear4_dp / valveLinear4_dp_nominal)**0.5 * (1 - f_pipe4),
    -valveLinear5_V_flow + valveLinear5_opening * valveLinear5_Flow_Nominal * (valveLinear5_dp / valveLinear5_dp_nominal)**0.5,
    -valveLinear6_V_flow + valveLinear6_opening * valveLinear6_Flow_Nominal * (valveLinear6_dp / valveLinear6_dp_nominal)**0.5 * (1 - f_valve6),
    
    # Tank level equations
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / (sym.pi * (tank1_Diameter / 2)**2),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    -der_tank2_level + (valveLinear2_V_flow - FI_16) / (sym.pi * (tank2_Diameter / 2)**2) - f_tank2leak,
    fdt.DiffConstraint('der_tank3_level', 'tank3_level'),
    -der_tank3_level + (valveLinear3_V_flow - FI_15) / (sym.pi * (tank3_Diameter / 2)**2),
    fdt.DiffConstraint('der_tank4_level', 'tank4_level'),
    -der_tank4_level + (FI_16 + valveLinear5_V_flow - FI_17) / (sym.pi * (tank4_Diameter / 2)**2),
    
    # Sensor equations
    -FI_13_eq + FI_13 - valveLinear1_V_flow,
    -LI_21_eq + LI_21 - der_tank1_level,
    -FI_14_eq + FI_14 - valveLinear2_V_flow,
    -LI_22_eq + LI_22 - der_tank2_level,
    -FI_15_eq + FI_15 - valveLinear3_V_flow,
    -LI_23_eq + LI_23 - der_tank3_level,
    -FI_16_eq + FI_16 - valveLinear4_V_flow,
    -LI_24_eq + LI_24 - der_tank4_level,
    -FI_17_eq + FI_17 - valveLinear6_V_flow
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_vars = ['tank1_level', 'tank2_level', 'tank3_level', 'tank4_level',
                   'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
                   'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow',
                   'FI_13_eq', 'LI_21_eq', 'FI_14_eq', 'LI_22_eq', 'FI_15_eq', 'LI_23_eq',
                   'FI_16_eq', 'LI_24_eq', 'FI_17_eq']
for var in additional_vars:
    if var not in model_def['x'] and var not in model_def['f'] and var not in model_def['z'] and var not in model_def['parameters']:
        model_def['x'].append(var)