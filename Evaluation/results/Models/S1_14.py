import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['tank1_m', 'der_tank1_m', 'valve0_dp', 'valve1_dp', 'tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_N_Nominal', 'pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Pump equation
    -FI_1 + pump_N / pump_N_Nominal * pump_V * (1 - f_pumpSlow),
    
    # Valve0 flow equation
    -FI_2 + valve0_opening * valve0_Flow_Nominal * sym.sqrt(1 - (valve0_dp / valve0_dp_nominal)**2) * (1 - f_valve0),
    
    # Valve1 flow equation
    -FI_4 + valve1_opening * valve1_Flow_Nominal * sym.sqrt(1 - (valve1_dp / valve1_dp_nominal)**2) * (1 - f_valve1),
    
    # Tank1 mass balance
    -der_tank1_m + FI_2 - FI_4 - f_tank1leak,
    
    # Tank1 level calculation based on mass and tank geometry
    -LI_3 + tank1_m / (sym.pi * (tank1_Diameter / 2)**2 * 1000),
    
    # Differential equation for tank1 mass
    fdt.DiffConstraint('der_tank1_m', 'tank1_m')
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur in any of the mentioned lists, add them under key 'x'
# Additional variables identified: 'pump_flow', 'valve0_flow', 'valve1_flow', 'tank1_level', 'der_tank1_level'
# 'pump_flow', 'valve0_flow', 'valve1_flow' are intermediate variables and do not need to be added to 'x'
# 'tank1_level' is already added to 'x'
# 'der_tank1_level' is not used in the model_def['rels'] and hence does not need to be added