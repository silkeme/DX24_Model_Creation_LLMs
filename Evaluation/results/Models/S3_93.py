import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
        'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow',
        'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level',
        'tank1_A', 'tank2_A', 'tank3_A', 'tank4_A'
    ],
    'f': [
        'f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'
    ],
    'z': [
        'FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17',
        'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening',
        'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'
    ],
    'parameters': [
        'pipe1_Length', 'pipe7_Length', 'pipe2_Length', 'pipe3_Length', 'pipe4_Length',
        'pipe5_Length', 'pipe6_Length', 'pipe1_Diameter', 'pipe7_Diameter', 'pipe2_Diameter',
        'pipe3_Diameter', 'pipe4_Diameter', 'pipe5_Diameter', 'pipe6_Diameter',
        'tank1_Height', 'tank2_Height', 'tank3_Height', 'tank4_Height',
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal',
        'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal',
        'valveLinear7_Flow_Nominal', 'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal',
        'valveLinear3_dp_nominal', 'valveLinear4_dp_nominal', 'valveLinear5_dp_nominal',
        'valveLinear6_dp_nominal', 'valveLinear7_dp_nominal'
    ],
    'rels': []
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Equations for the flow through each valve
model_def['rels'].append(-valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal)
model_def['rels'].append(-valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (1 - f_valve3))
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal)
model_def['rels'].append(-valveLinear4_V_flow + valveLinear4_opening * valveLinear4_Flow_Nominal * (1 - f_pipe4))
model_def['rels'].append(-valveLinear5_V_flow + valveLinear5_opening * valveLinear5_Flow_Nominal)
model_def['rels'].append(-valveLinear6_V_flow + valveLinear6_opening * valveLinear6_Flow_Nominal * (1 - f_valve6))

# Equations for the water level in each tank
model_def['rels'].append(-tank1_A + (tank1_Diameter / 2) ** 2 * 3.14159)
model_def['rels'].append(-tank2_A + (tank2_Diameter / 2) ** 2 * 3.14159)
model_def['rels'].append(-tank3_A + (tank3_Diameter / 2) ** 2 * 3.14159)
model_def['rels'].append(-tank4_A + (tank4_Diameter / 2) ** 2 * 3.14159)

model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(-der_tank1_level + (FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / tank1_A)
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))
model_def['rels'].append(-der_tank2_level + (valveLinear2_V_flow - FI_16) / tank2_A - f_tank2leak)
model_def['rels'].append(fdt.DiffConstraint('der_tank3_level', 'tank3_level'))
model_def['rels'].append(-der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / tank3_A)
model_def['rels'].append(fdt.DiffConstraint('der_tank4_level', 'tank4_level'))
model_def['rels'].append(-der_tank4_level + (valveLinear4_V_flow + valveLinear5_V_flow - FI_17) / tank4_A)

# Sensor equations
model_def['rels'].append(-FI_13 + valveLinear1_V_flow)
model_def['rels'].append(-LI_21 + der_tank1_level)
model_def['rels'].append(-FI_14 + valveLinear2_V_flow)
model_def['rels'].append(-LI_22 + der_tank2_level)
model_def['rels'].append(-FI_15 + valveLinear3_V_flow)
model_def['rels'].append(-LI_23 + der_tank3_level)
model_def['rels'].append(-FI_16 + valveLinear4_V_flow)
model_def['rels'].append(-LI_24 + der_tank4_level)
model_def['rels'].append(-FI_17 + valveLinear6_V_flow)

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_variables = ['tank1_level', 'tank2_level', 'tank3_level', 'tank4_level']
for var in additional_variables:
    if var not in model_def['x']:
        model_def['x'].append(var)

sym.var(model_def['x'])  # Update the symbols for the newly added variables