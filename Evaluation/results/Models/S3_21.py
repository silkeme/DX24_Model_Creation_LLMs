import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'valveLinear1_dp', 'valveLinear2_dp', 'valveLinear3_dp', 'valveLinear4_dp', 'valveLinear5_dp', 'valveLinear6_dp',
        'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level',
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow', 'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow',
        'tank1_cross_sectional_area', 'tank2_cross_sectional_area', 'tank3_cross_sectional_area', 'tank4_cross_sectional_area'
    ],
    'f': [
        'f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'
    ],
    'z': [
        'FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17',
        'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening', 'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'
    ],
    'parameters': [
        'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter',
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal',
        'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'valveLinear4_dp_nominal', 'valveLinear5_dp_nominal', 'valveLinear6_dp_nominal'
    ],
    'rels': []
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Valve flow equations
model_def['rels'].append(-valveLinear1_V_flow + valveLinear1_Flow_Nominal * valveLinear1_opening * sym.sqrt(1 - (valveLinear1_dp / valveLinear1_dp_nominal)**2))
model_def['rels'].append(-valveLinear2_V_flow + valveLinear2_Flow_Nominal * valveLinear2_opening * sym.sqrt(1 - (valveLinear2_dp / valveLinear2_dp_nominal)**2))
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_Flow_Nominal * valveLinear3_opening * sym.sqrt(1 - (valveLinear3_dp / valveLinear3_dp_nominal)**2))
model_def['rels'].append(-valveLinear4_V_flow + valveLinear4_Flow_Nominal * valveLinear4_opening * sym.sqrt(1 - (valveLinear4_dp / valveLinear4_dp_nominal)**2))
model_def['rels'].append(-valveLinear5_V_flow + valveLinear5_Flow_Nominal * valveLinear5_opening * sym.sqrt(1 - (valveLinear5_dp / valveLinear5_dp_nominal)**2))
model_def['rels'].append(-valveLinear6_V_flow + valveLinear6_Flow_Nominal * valveLinear6_opening * sym.sqrt(1 - (valveLinear6_dp / valveLinear6_dp_nominal)**2))

# Tank cross-sectional area equations
model_def['rels'].append(-tank1_cross_sectional_area + (tank1_Diameter / 2)**2 * sym.pi)
model_def['rels'].append(-tank2_cross_sectional_area + (tank2_Diameter / 2)**2 * sym.pi)
model_def['rels'].append(-tank3_cross_sectional_area + (tank3_Diameter / 2)**2 * sym.pi)
model_def['rels'].append(-tank4_cross_sectional_area + (tank4_Diameter / 2)**2 * sym.pi)

# Tank level derivative equations
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level') - ((FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / tank1_cross_sectional_area))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level') - ((valveLinear2_V_flow - valveLinear4_V_flow) / tank2_cross_sectional_area - f_tank2leak))
model_def['rels'].append(fdt.DiffConstraint('der_tank3_level', 'tank3_level') - ((valveLinear3_V_flow - valveLinear5_V_flow) / tank3_cross_sectional_area))
model_def['rels'].append(fdt.DiffConstraint('der_tank4_level', 'tank4_level') - ((valveLinear4_V_flow + valveLinear5_V_flow - FI_17) / tank4_cross_sectional_area))

# Sensor equations
model_def['rels'].append(-FI_13 + valveLinear1_V_flow)
model_def['rels'].append(-LI_21 + der_tank1_level)
model_def['rels'].append(-FI_14 + valveLinear2_V_flow)
model_def['rels'].append(-LI_22 + der_tank2_level)
model_def['rels'].append(-FI_15 + valveLinear3_V_flow * (1 - f_valve3))
model_def['rels'].append(-LI_23 + der_tank3_level)
model_def['rels'].append(-FI_16 + valveLinear4_V_flow * (1 - f_pipe4))
model_def['rels'].append(-LI_24 + der_tank4_level)
model_def['rels'].append(-FI_17 + valveLinear6_V_flow * (1 - f_valve6))

# Add missing variables to 'x' if they are not already in 'x', 'f', 'z', or 'parameters'
additional_vars = ['tank1_level', 'tank2_level', 'tank3_level', 'tank4_level']
for var in additional_vars:
    if var not in model_def['x'] and var not in model_def['f'] and var not in model_def['z'] and var not in model_def['parameters']:
        model_def['x'].append(var)

# Now the model is ready to be used with the faultdiagnosistoolbox