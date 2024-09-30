import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['der_tank1_level', 'der_tank_level', 'der_tank2_level', 'tank1_level', 'tank_level', 'tank2_level', 'pump_flow', 'pump1_flow', 'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow'],
    'f': ['f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'],
    'z': ['FI_1', 'LI_2', 'FI_3', 'LI_4', 'FI_5', 'LI_6', 'FI_7', 'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'],
    'parameters': ['tank1_Diameter', 'tank_Diameter', 'tank2_Diameter', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'pump_V', 'pump1_V', 'time']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Pump equations
    -pump_flow + pump_N * pump_V,
    -pump1_flow + pump1_N * pump1_V,
    
    # Tank level derivative equations
    -der_tank1_level + (pump_flow - valveLinear1_V_flow - f_tank1leak) / (3.1415 * (tank1_Diameter / 2) ** 2),
    -der_tank_level + (valveLinear1_V_flow - pump1_flow) / (3.1415 * (tank_Diameter / 2) ** 2),
    -der_tank2_level + (pump1_flow - valveLinear3_V_flow - f_tank2leak) / (3.1415 * (tank2_Diameter / 2) ** 2),
    
    # Valve flow equations
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1),
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (1 - f_valve2),
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3),
    
    # Sensor equations
    -FI_1 + pump_flow,
    -LI_2 + tank1_level,
    -FI_3 + valveLinear1_V_flow,
    -LI_4 + tank_level,
    -FI_5 + pump1_flow,
    -LI_6 + tank2_level,
    -FI_7 + valveLinear3_V_flow,
    
    # Differential equations for tank levels
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    fdt.DiffConstraint('der_tank_level', 'tank_level'),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level')
]