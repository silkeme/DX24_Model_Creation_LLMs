import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow', 'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow', 'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level'],
    'f': ['f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'],
    'z': ['FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening', 'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'],
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
    
    # Tank level differential equations
    fdt.DiffConstraint('der_tank1_level', '(FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / (3.141592653589793 * (tank1_Diameter / 2) ** 2)'),
    fdt.DiffConstraint('der_tank2_level', '(valveLinear2_V_flow - valveLinear4_V_flow) / (3.141592653589793 * (tank2_Diameter / 2) ** 2) - f_tank2leak'),
    fdt.DiffConstraint('der_tank3_level', '(valveLinear3_V_flow - valveLinear5_V_flow) / (3.141592653589793 * (tank3_Diameter / 2) ** 2)'),
    fdt.DiffConstraint('der_tank4_level', '(valveLinear4_V_flow + valveLinear5_V_flow - FI_17) / (3.141592653589793 * (tank4_Diameter / 2) ** 2)'),
    
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