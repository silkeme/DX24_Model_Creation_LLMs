import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'pump1_flow', 'der_tank1_level', 'der_tank_level', 'der_tank2_level', 'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow', 'outlet1_flow', 'outlet2_flow', 'tank1_level', 'tank_level', 'tank2_level'],
    'f': ['f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'],
    'z': ['FI1', 'LI2', 'FI3', 'LI4', 'FI5', 'LI6', 'FI7', 'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'],
    'parameters': ['pipe_Length', 'pipe4_Length', 'pipe5_Length', 'pipe1_Length', 'pipe2_Length', 'pipe6_Length', 'pipe7_Length', 'pipe8_Length', 'pipe_Diameter', 'pipe4_Diameter', 'pipe5_Diameter', 'pipe1_Diameter', 'pipe2_Diameter', 'pipe6_Diameter', 'pipe7_Diameter', 'pipe3_Diameter', 'tank_Height', 'tank1_Height', 'tank2_Height', 'pump_N_Nominal', 'pump1_N_Nominal', 'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'tank1_Diameter', 'tank_Diameter', 'tank2_Diameter', 'pump_V', 'pump1_V', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Pump equations
    -pump_flow + pump_N * pump_V,
    -pump1_flow + pump1_N * pump1_V,
    
    # Tank level differential equations
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -(der_tank1_level - (pump_flow - valveLinear1_V_flow - f_tank1leak) / (3.14159 * (tank1_Diameter / 2) ** 2)),
    fdt.DiffConstraint('der_tank_level', 'tank_level'),
    -(der_tank_level - (valveLinear1_V_flow - pump1_flow - f_valve1) / (3.14159 * (tank_Diameter / 2) ** 2)),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    -(der_tank2_level - (pump_flow - valveLinear3_V_flow - f_tank2leak) / (3.14159 * (tank2_Diameter / 2) ** 2)),
    
    # Valve flow equations
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1),
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (1 - f_valve2),
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3),
    
    # Outlet flow equations
    -outlet1_flow + valveLinear2_V_flow,
    -outlet2_flow + valveLinear3_V_flow,
    
    # Sensor equations
    -FI1 + pump_flow,
    -LI2 + tank1_level,
    -FI3 + valveLinear1_V_flow,
    -LI4 + tank_level,
    -FI5 + pump1_flow,
    -LI6 + tank2_level,
    -FI7 + valveLinear3_V_flow
]