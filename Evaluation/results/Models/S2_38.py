import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['tank1_level', 'tank_level', 'tank2_level', 'der_tank1_level', 'der_tank_level', 'der_tank2_level'],  # unknown variables
    'f': ['f_tank1leak', 'f_tank2leak', 'f_valve1', 'f_valve2', 'f_valve3'],  # faults
    'z': ['FI_1', 'LI_2', 'FI_3', 'LI_4', 'FI_5', 'LI_6', 'FI_7', 'pump_N', 'pump1_N', 'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening'],  # known variables
    'parameters': [
        'pipe_Length', 'pipe4_Length', 'pipe5_Length', 'pipe1_Length', 'pipe2_Length', 'pipe6_Length', 'pipe7_Length', 'pipe8_Length',
        'pipe_Diameter', 'pipe4_Diameter', 'pipe5_Diameter', 'pipe1_Diameter', 'pipe2_Diameter', 'pipe6_Diameter', 'pipe7_Diameter', 'pipe3_Diameter',
        'tank_Diameter', 'tank1_Diameter', 'tank2_Diameter', 'tank_Height', 'tank1_Height', 'tank2_Height',
        'pump_N_Nominal', 'pump1_N_Nominal', 'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal',
        'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'pump_V', 'pump1_V'
    ]  # parameters
}

# Define the symbols for sympy
sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Store the equations in the model definition
model_def['rels'] = [
    # Equations for pumps
    -FI_1 + pump_N * pump_V,
    -FI_5 + pump1_N * pump1_V,
    
    # Equations for tanks
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (pump_N * pump_V - valveLinear1_opening * valveLinear1_Flow_Nominal) / (sym.pi * (tank1_Diameter / 2) ** 2) - f_tank1leak,
    
    fdt.DiffConstraint('der_tank_level', 'tank_level'),
    -der_tank_level + (valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1) - pump1_N * pump1_V) / (sym.pi * (tank_Diameter / 2) ** 2),
    
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    -der_tank2_level + (pump1_N * pump1_V - valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3)) / (sym.pi * (tank2_Diameter / 2) ** 2) - f_tank2leak,
    
    # Equations for valves
    -FI_3 + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1),
    -FI_7 + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3),
    
    # Matching sensors with variables
    -FI_1 + pump_N * pump_V,
    -LI_2 + tank1_level,
    -FI_3 + valveLinear1_opening * valveLinear1_Flow_Nominal * (1 - f_valve1),
    -LI_4 + tank_level,
    -FI_5 + pump1_N * pump1_V,
    -LI_6 + tank2_level,
    -FI_7 + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3)
]

# Remove the now empty variable list
# del variables  # This line is commented out because 'variables' is not defined in the provided code snippet