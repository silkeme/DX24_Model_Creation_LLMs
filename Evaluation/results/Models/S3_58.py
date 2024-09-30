import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level',
        'tank1_level', 'tank2_level', 'tank3_level', 'tank4_level',
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
        'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow',
        'tank1_A', 'tank2_A', 'tank3_A', 'tank4_A'
    ],
    'f': [
        'f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'
    ],
    'z': [
        'FI13', 'LI21', 'FI14', 'LI22', 'FI15', 'LI23', 'FI16', 'LI24', 'FI17',
        'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening',
        'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'
    ],
    'parameters': [
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal',
        'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal',
        'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter'
    ],
    'rels': []
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Valve flow rates equations
model_def['rels'].append(-valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal)
model_def['rels'].append(-valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (1 - f_valve3))
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal)
model_def['rels'].append(-valveLinear4_V_flow + valveLinear4_opening * valveLinear4_Flow_Nominal * (1 - f_pipe4))
model_def['rels'].append(-valveLinear5_V_flow + valveLinear5_opening * valveLinear5_Flow_Nominal)
model_def['rels'].append(-valveLinear6_V_flow + valveLinear6_opening * valveLinear6_Flow_Nominal * (1 - f_valve6))

# Tank cross-sectional area equations
model_def['rels'].append(-tank1_A + 3.14159 * (tank1_Diameter ** 2) / 4)
model_def['rels'].append(-tank2_A + 3.14159 * (tank2_Diameter ** 2) / 4)
model_def['rels'].append(-tank3_A + 3.14159 * (tank3_Diameter ** 2) / 4)
model_def['rels'].append(-tank4_A + 3.14159 * (tank4_Diameter ** 2) / 4)

# Differential equations for tank levels
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(-der_tank1_level + (FI13 - valveLinear2_V_flow - valveLinear3_V_flow) / tank1_A)
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))
model_def['rels'].append(-der_tank2_level + (valveLinear2_V_flow - valveLinear4_V_flow) / tank2_A - f_tank2leak)
model_def['rels'].append(fdt.DiffConstraint('der_tank3_level', 'tank3_level'))
model_def['rels'].append(-der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / tank3_A)
model_def['rels'].append(fdt.DiffConstraint('der_tank4_level', 'tank4_level'))
model_def['rels'].append(-der_tank4_level + (valveLinear4_V_flow + valveLinear5_V_flow - valveLinear6_V_flow) / tank4_A)

# Sensor equations
model_def['rels'].append(-FI13 + valveLinear1_V_flow)
model_def['rels'].append(-LI21 + tank1_level)
model_def['rels'].append(-FI14 + valveLinear2_V_flow)
model_def['rels'].append(-LI22 + tank2_level)
model_def['rels'].append(-FI15 + valveLinear3_V_flow)
model_def['rels'].append(-LI23 + tank3_level)
model_def['rels'].append(-FI16 + valveLinear4_V_flow + valveLinear5_V_flow)
model_def['rels'].append(-LI24 + tank4_level)
model_def['rels'].append(-FI17 + valveLinear6_V_flow)