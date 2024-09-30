import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'der_pump_medium_h', 'der_tank1_level', 'der_tank_level', 'der_pump1_medium_h', 'der_tank2_level',
        'pump_Q', 'tank1_Q_in', 'tank1_Q_out', 'tank_Q_in', 'tank_Q_out', 'pump1_Q', 'valveLinear2_V_flow',
        'tank2_Q_in', 'tank2_Q_out', 'valveLinear3_V_flow'
    ],
    'f': [
        'f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'
    ],
    'z': [
        'FI_1', 'LI_2', 'FI_3', 'LI_4', 'FI_5', 'LI_6', 'FI_7',
        'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'
    ],
    'parameters': [
        'pipe_Length', 'pipe4_Length', 'pipe5_Length', 'pipe1_Length', 'pipe2_Length', 'pipe6_Length',
        'pipe7_Length', 'pipe8_Length', 'pipe_Diameter', 'pipe4_Diameter', 'pipe5_Diameter', 'pipe1_Diameter',
        'pipe2_Diameter', 'pipe6_Diameter', 'pipe7_Diameter', 'pipe3_Diameter', 'tank_Diameter', 'tank1_Diameter',
        'tank2_Diameter', 'tank_Height', 'tank1_Height', 'tank2_Height', 'pump_N_Nominal', 'pump1_N_Nominal',
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal',
        'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'pump_V', 'pump1_V'
    ],
    'rels': []
}

# Create the variables
sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Define the equations and add them to the 'rels' list
model_def['rels'].append(-der_pump_medium_h + pump_N / pump_N_Nominal * pump_V / (sym.pi * (tank_Diameter / 2) ** 2))
model_def['rels'].append(-der_tank1_level + (pump_Q - valveLinear1_opening * valveLinear1_Flow_Nominal) / (sym.pi * (tank1_Diameter / 2) ** 2) - f_tank1leak)
model_def['rels'].append(-valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal - f_valve1)
model_def['rels'].append(-der_tank_level + (valveLinear1_V_flow - pump1_N / pump1_N_Nominal * pump1_V) / (sym.pi * (tank_Diameter / 2) ** 2))
model_def['rels'].append(-der_pump1_medium_h + pump1_N / pump1_N_Nominal * pump1_V / (sym.pi * (tank_Diameter / 2) ** 2))
model_def['rels'].append(-valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal - f_valve2)
model_def['rels'].append(-der_tank2_level + (pump_Q - valveLinear3_opening * valveLinear3_Flow_Nominal) / (sym.pi * (tank2_Diameter / 2) ** 2) - f_tank2leak)
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal - f_valve3)
model_def['rels'].append(-FI_1 + pump_Q)
model_def['rels'].append(-LI_2 + der_tank1_level)
model_def['rels'].append(-FI_3 + valveLinear1_V_flow)
model_def['rels'].append(-LI_4 + der_tank_level)
model_def['rels'].append(-FI_5 + pump1_Q)
model_def['rels'].append(-LI_6 + der_tank2_level)
model_def['rels'].append(-FI_7 + valveLinear3_V_flow)

# Add differential constraints
model_def['rels'].append(fdt.DiffConstraint('der_pump_medium_h', 'pump_medium_h'))
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank_level', 'tank_level'))
model_def['rels'].append(fdt.DiffConstraint('der_pump1_medium_h', 'pump1_medium_h'))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_variables = ['pump_medium_h', 'tank1_level', 'tank_level', 'pump1_medium_h', 'tank2_level']
for var in additional_variables:
    if var not in model_def['x']:
        model_def['x'].append(var)

# Now the model is ready to be used with the faultdiagnosis toolbox