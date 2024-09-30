import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'pump_flow', 'pump1_flow',
        'der_tank1_level', 'der_tank2_level', 'der_tank_level',
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
        'tank1_level', 'tank_level', 'tank2_level'
    ],
    'f': ['f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'],
    'z': [
        'FI_1', 'LI_2', 'FI_3', 'LI_4', 'FI_5', 'LI_6', 'FI_7',
        'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'
    ],
    'parameters': [
        'tank1_Diameter', 'tank2_Diameter', 'tank_Diameter',
        'pump_V', 'pump1_V',
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal'
    ],
    'rels': []
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Equations for pumps
model_def['rels'].append(-pump_flow + pump_N * pump_V)
model_def['rels'].append(-pump1_flow + pump1_N * pump1_V)

# Equations for tanks
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(-der_tank1_level + (pump_flow - valveLinear1_V_flow) / (sym.pi * (tank1_Diameter / 2) ** 2) - f_tank1leak)

model_def['rels'].append(fdt.DiffConstraint('der_tank_level', 'tank_level'))
model_def['rels'].append(-der_tank_level + (valveLinear1_V_flow - pump1_flow) / (sym.pi * (tank_Diameter / 2) ** 2))

model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))
model_def['rels'].append(-der_tank2_level + (pump_flow - valveLinear3_V_flow) / (sym.pi * (tank2_Diameter / 2) ** 2) - f_tank2leak)

# Equations for valves
model_def['rels'].append(-valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1))
model_def['rels'].append(-valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (1 - f_valve2))
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3))

# Matching sensors with variables
model_def['rels'].append(-FI_1 + pump_flow)
model_def['rels'].append(-LI_2 + tank1_level)
model_def['rels'].append(-FI_3 + valveLinear1_V_flow)
model_def['rels'].append(-LI_4 + tank_level)
model_def['rels'].append(-FI_5 + pump1_flow)
model_def['rels'].append(-LI_6 + tank2_level)
model_def['rels'].append(-FI_7 + valveLinear3_V_flow)