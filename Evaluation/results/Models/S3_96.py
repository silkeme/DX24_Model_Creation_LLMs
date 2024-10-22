import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'valveLinear1_V_flow', 'valveLinear1_dp', 'valveLinear2_V_flow', 'valveLinear2_dp', 
        'valveLinear3_V_flow', 'valveLinear3_dp', 'valveLinear4_V_flow', 'valveLinear4_dp', 
        'valveLinear5_V_flow', 'valveLinear5_dp', 'valveLinear6_V_flow', 'valveLinear6_dp', 
        'der_tank1_level', 'tank1_level', 'der_tank2_level', 'tank2_level', 
        'der_tank3_level', 'tank3_level', 'der_tank4_level', 'tank4_level'
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
        'valveLinear1_Flow_Nominal', 'valveLinear1_dp_nominal', 'valveLinear2_Flow_Nominal', 
        'valveLinear2_dp_nominal', 'valveLinear3_Flow_Nominal', 'valveLinear3_dp_nominal', 
        'valveLinear4_Flow_Nominal', 'valveLinear4_dp_nominal', 'valveLinear5_Flow_Nominal', 
        'valveLinear5_dp_nominal', 'valveLinear6_Flow_Nominal', 'valveLinear6_dp_nominal', 
        'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter'
    ],
    'rels': []
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Equations
model_def['rels'].append(-valveLinear1_V_flow + valveLinear1_Flow_Nominal * valveLinear1_opening * sym.sqrt(1 - (valveLinear1_dp / valveLinear1_dp_nominal)**2))
model_def['rels'].append(-valveLinear2_V_flow + valveLinear2_Flow_Nominal * valveLinear2_opening * sym.sqrt(1 - (valveLinear2_dp / valveLinear2_dp_nominal)**2))
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_Flow_Nominal * valveLinear3_opening * sym.sqrt(1 - (valveLinear3_dp / valveLinear3_dp_nominal)**2))
model_def['rels'].append(-valveLinear4_V_flow + valveLinear4_Flow_Nominal * valveLinear4_opening * sym.sqrt(1 - (valveLinear4_dp / valveLinear4_dp_nominal)**2))
model_def['rels'].append(-valveLinear5_V_flow + valveLinear5_Flow_Nominal * valveLinear5_opening * sym.sqrt(1 - (valveLinear5_dp / valveLinear5_dp_nominal)**2))
model_def['rels'].append(-valveLinear6_V_flow + valveLinear6_Flow_Nominal * valveLinear6_opening * sym.sqrt(1 - (valveLinear6_dp / valveLinear6_dp_nominal)**2))

model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(-der_tank1_level + (FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / (sym.pi * (tank1_Diameter / 2)**2))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))
model_def['rels'].append(-der_tank2_level + (valveLinear2_V_flow - FI_16) / (sym.pi * (tank2_Diameter / 2)**2) - f_tank2leak)
model_def['rels'].append(fdt.DiffConstraint('der_tank3_level', 'tank3_level'))
model_def['rels'].append(-der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / (sym.pi * (tank3_Diameter / 2)**2))
model_def['rels'].append(fdt.DiffConstraint('der_tank4_level', 'tank4_level'))
model_def['rels'].append(-der_tank4_level + (FI_16 + valveLinear5_V_flow - FI_17) / (sym.pi * (tank4_Diameter / 2)**2))

model_def['rels'].append(-valveLinear1_dp + LI_21 * 9.81)
model_def['rels'].append(-valveLinear2_dp + (LI_21 - LI_22) * 9.81)
model_def['rels'].append(-valveLinear3_dp + (LI_21 - LI_23) * 9.81)
model_def['rels'].append(-valveLinear4_dp + (LI_22 - LI_24) * 9.81)
model_def['rels'].append(-valveLinear5_dp + (LI_23 - LI_24) * 9.81)
model_def['rels'].append(-valveLinear6_dp + LI_24 * 9.81)

# Sensor equations
model_def['rels'].append(-FI_13 + valveLinear1_V_flow)
model_def['rels'].append(-LI_21 + tank1_level)
model_def['rels'].append(-FI_14 + valveLinear2_V_flow)
model_def['rels'].append(-LI_22 + tank2_level)
model_def['rels'].append(-FI_15 + valveLinear3_V_flow)
model_def['rels'].append(-LI_23 + tank3_level)
model_def['rels'].append(-FI_16 + valveLinear4_V_flow * (1 - f_pipe4))
model_def['rels'].append(-LI_24 + tank4_level)
model_def['rels'].append(-FI_17 + valveLinear6_V_flow * (1 - f_valve6))

# Faults in the equations
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_V_flow * (1 - f_valve3))

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur, add them under key 'x'
# No need to add any variables as they are all already present in the lists

# Now the model is ready to be used with the faultdiagnosis toolbox