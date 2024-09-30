import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'pump1_flow', 'der_tank1_level', 'der_tank2_level', 'der_tank_level', 'tank1_level', 'tank_level', 'tank2_level'],
    'f': ['f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'],
    'z': ['FI1', 'LI2', 'FI3', 'LI4', 'FI5', 'LI6', 'FI7', 'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'],
    'parameters': ['tank_Diameter', 'tank1_Diameter', 'tank2_Diameter', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'pump_V', 'pump1_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations for pumps
    -pump_flow + pump_N * pump_V,
    -pump1_flow + pump1_N * pump1_V,
    
    # Equations for tanks
    -der_tank1_level + (pump_flow - valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1) - f_tank1leak) / (sym.pi * (tank1_Diameter / 2) ** 2),
    -der_tank2_level + (pump1_flow - valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3) - f_tank2leak) / (sym.pi * (tank2_Diameter / 2) ** 2),
    -der_tank_level + (valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1) - pump1_flow) / (sym.pi * (tank_Diameter / 2) ** 2),
    
    # Equations for valves already included in tank equations
    
    # Sensor equations
    -FI1 + pump_flow,
    -LI2 + tank1_level,
    -FI3 + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1),
    -LI4 + tank_level,
    -FI5 + pump1_flow,
    -LI6 + tank2_level,
    -FI7 + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3),
    
    # Differential equations
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    fdt.DiffConstraint('der_tank_level', 'tank_level')
]