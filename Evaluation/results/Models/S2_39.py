import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'pump_flow', 'pump1_flow',
        'der_tank1_level', 'der_tank2_level', 'der_tank_level',
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
        'tank1_level', 'tank2_level', 'tank_level',
        'valveLinear1_dp', 'valveLinear2_dp', 'valveLinear3_dp'
    ],
    'f': [
        'f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'
    ],
    'z': [
        'FI_1', 'LI_2', 'FI_3', 'LI_4', 'FI_5', 'LI_6', 'FI_7',
        'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'
    ],
    'parameters': [
        'pipe_Length', 'pipe4_Length', 'pipe5_Length', 'pipe1_Length', 'pipe2_Length', 'pipe6_Length', 'pipe7_Length',
        'pipe8_Length', 'pipe_Diameter', 'pipe4_Diameter', 'pipe5_Diameter', 'pipe1_Diameter', 'pipe2_Diameter',
        'pipe6_Diameter', 'pipe7_Diameter', 'pipe3_Diameter', 'tank_Diameter', 'tank1_Diameter', 'tank2_Diameter',
        'tank_Height', 'tank1_Height', 'tank2_Height', 'pump_N_Nominal', 'pump1_N_Nominal', 'valveLinear1_Flow_Nominal',
        'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal',
        'valveLinear3_dp_nominal', 'pump_V', 'pump1_V'
    ],
    'rels': []
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Equations for pumps
model_def['rels'].append(-sym.var('pump_flow') + sym.var('pump_N') / sym.var('pump_N_Nominal') * sym.var('pump_V'))
model_def['rels'].append(-sym.var('pump1_flow') + sym.var('pump1_N') / sym.var('pump1_N_Nominal') * sym.var('pump1_V'))

# Equations for tanks
model_def['rels'].append(-sym.var('der_tank1_level') + (sym.var('pump_flow') - sym.var('valveLinear1_V_flow') - sym.var('f_tank1leak')) / (sym.pi * (sym.var('tank1_Diameter') / 2) ** 2))
model_def['rels'].append(-sym.var('der_tank2_level') + (sym.var('pump_flow') - sym.var('valveLinear3_V_flow') - sym.var('f_tank2leak')) / (sym.pi * (sym.var('tank2_Diameter') / 2) ** 2))
model_def['rels'].append(-sym.var('der_tank_level') + (sym.var('valveLinear1_V_flow') - sym.var('pump1_flow')) / (sym.pi * (sym.var('tank_Diameter') / 2) ** 2))

# Equations for valves
model_def['rels'].append(-sym.var('valveLinear1_V_flow') + sym.var('valveLinear1_opening') * sym.var('valveLinear1_Flow_Nominal') * (1 - sym.var('valveLinear1_dp') / sym.var('valveLinear1_dp_nominal')) * (1 - sym.var('f_valve1')))
model_def['rels'].append(-sym.var('valveLinear2_V_flow') + sym.var('valveLinear2_opening') * sym.var('valveLinear2_Flow_Nominal') * (1 - sym.var('valveLinear2_dp') / sym.var('valveLinear2_dp_nominal')) * (1 - sym.var('f_valve2')))
model_def['rels'].append(-sym.var('valveLinear3_V_flow') + sym.var('valveLinear3_opening') * sym.var('valveLinear3_Flow_Nominal') * (1 - sym.var('valveLinear3_dp') / sym.var('valveLinear3_dp_nominal')) * (1 - sym.var('f_valve3')))

# Sensor equations
model_def['rels'].append(-sym.var('FI_1') + sym.var('pump_flow'))
model_def['rels'].append(-sym.var('LI_2') + sym.var('tank1_level'))
model_def['rels'].append(-sym.var('FI_3') + sym.var('valveLinear1_V_flow'))
model_def['rels'].append(-sym.var('LI_4') + sym.var('tank_level'))
model_def['rels'].append(-sym.var('FI_5') + sym.var('pump1_flow'))
model_def['rels'].append(-sym.var('LI_6') + sym.var('tank2_level'))
model_def['rels'].append(-sym.var('FI_7') + sym.var('valveLinear3_V_flow'))

# Differential equations
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank_level', 'tank_level'))

# Output the complete model
print(model_def)