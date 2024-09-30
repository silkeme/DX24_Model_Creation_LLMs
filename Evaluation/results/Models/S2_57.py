import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['der_tank1_level', 'der_tank_level', 'der_tank2_level', 'tank1_level', 'tank_level', 'tank2_level', 'pump_flow', 'pump1_flow', 'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow'],
    'f': ['f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'],
    'z': ['FI1', 'LI2', 'FI3', 'LI4', 'FI5', 'LI6', 'FI7', 'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'],
    'parameters': ['tank1_Diameter', 'tank_Diameter', 'tank2_Diameter', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'pump_V', 'pump1_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Pump equations
    -pump_flow + pump_N * pump_V,
    -pump1_flow + pump1_N * pump1_V,
    
    # Tank level equations based on incompressible fluid assumption
    -der_tank1_level + (pump_flow - valveLinear1_V_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    -der_tank_level + (valveLinear1_V_flow - pump1_flow) / (sym.pi * (tank_Diameter / 2) ** 2),
    -der_tank2_level + (pump1_flow - valveLinear3_V_flow - f_tank2leak) / (sym.pi * (tank2_Diameter / 2) ** 2),
    
    # Valve flow equations based on linear valve characteristics and no energy losses
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1),
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * (1 - f_valve2),
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3),
    
    # Sensor equations
    -FI1 + pump_flow,
    -LI2 + tank1_level,
    -FI3 + valveLinear1_V_flow,
    -LI4 + tank_level,
    -FI5 + pump1_flow,
    -LI6 + tank2_level,
    -FI7 + valveLinear3_V_flow
]

# Differential equations need to be added as DiffConstraints
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank_level', 'tank_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
additional_vars = ['time']
for var in additional_vars:
    if var not in model_def['x']:
        model_def['x'].append(var)

# Now the model is ready to be used with the faultdiagnosis toolbox