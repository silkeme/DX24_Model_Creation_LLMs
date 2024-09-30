import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'pump_flow', 'pump1_flow', 'der_tank1_level', 'der_tank_level', 'der_tank2_level',
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
        'tank1_m', 'tank_m', 'tank2_m', 'tank1_level', 'tank_level', 'tank2_level'
    ],
    'f': [
        'f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'
    ],
    'z': [
        'FI1', 'LI2', 'FI3', 'LI4', 'FI5', 'LI6', 'FI7',
        'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'
    ],
    'parameters': [
        'pipe_Length', 'pipe4_Length', 'pipe5_Length', 'pipe1_Length', 'pipe2_Length', 'pipe6_Length',
        'pipe7_Length', 'pipe8_Length', 'pipe_Diameter', 'pipe4_Diameter', 'pipe5_Diameter',
        'pipe1_Diameter', 'pipe2_Diameter', 'pipe6_Diameter', 'pipe7_Diameter', 'pipe3_Diameter',
        'tank_Diameter', 'tank1_Diameter', 'tank2_Diameter', 'tank_Height', 'tank1_Height',
        'tank2_Height', 'pump_N_Nominal', 'pump1_N_Nominal', 'valveLinear1_Flow_Nominal',
        'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'valveLinear1_dp_nominal',
        'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'pump_V', 'pump1_V'
    ],
    'rels': []
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Pump equations
model_def['rels'].append(-pump_flow + pump_N * pump_V)
model_def['rels'].append(-pump1_flow + pump1_N * pump1_V)

# Tank level equations based on incompressible fluid assumption
model_def['rels'].append(-der_tank1_level + (pump_flow - valveLinear1_V_flow) / (sym.pi * (tank1_Diameter / 2) ** 2) - f_tank1leak)
model_def['rels'].append(-der_tank_level + (valveLinear1_V_flow - pump1_flow) / (sym.pi * (tank_Diameter / 2) ** 2))
model_def['rels'].append(-der_tank2_level + (pump1_flow - valveLinear3_V_flow) / (sym.pi * (tank2_Diameter / 2) ** 2) - f_tank2leak)

# Valve flow equations based on linear valve characteristics and no energy losses
model_def['rels'].append(-valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1))
model_def['rels'].append(-valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (1 - f_valve2))
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3))

# Tank water level as a function of volume
model_def['rels'].append(-tank1_level + tank1_m / (sym.pi * (tank1_Diameter / 2) ** 2 * tank1_Height))
model_def['rels'].append(-tank_level + tank_m / (sym.pi * (tank_Diameter / 2) ** 2 * tank_Height))
model_def['rels'].append(-tank2_level + tank2_m / (sym.pi * (tank2_Diameter / 2) ** 2 * tank2_Height))

# Sensor equations
model_def['rels'].append(-FI1 + pump_flow)
model_def['rels'].append(-LI2 + tank1_level)
model_def['rels'].append(-FI3 + valveLinear1_V_flow)
model_def['rels'].append(-LI4 + tank_level)
model_def['rels'].append(-FI5 + pump1_flow)
model_def['rels'].append(-LI6 + tank2_level)
model_def['rels'].append(-FI7 + valveLinear3_V_flow)

# Differential equations
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_m'))
model_def['rels'].append(fdt.DiffConstraint('der_tank_level', 'tank_m'))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_m'))