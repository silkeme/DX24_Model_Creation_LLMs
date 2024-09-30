import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'tank1_Area', 'der_tank1_level', 'tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pipe_Diameter', 'pipe4_Diameter', 'tank1_Diameter', 'pipe1_Diameter', 'pipe2_Diameter', 'pipe_Length', 'pipe4_Length', 'pipe1_Length', 'pipe2_Length', 'tank1_Height', 'pump_N_Nominal', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'pump_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations
    -pump_V_flow + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_V_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    -valve1_V_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    -tank1_Area + (tank1_Diameter / 2) ** 2 * 3.14159,
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_V_flow - valve1_V_flow - f_tank1leak) / tank1_Area,
    
    # Sensor equations
    -FI_1 + pump_V_flow,
    -FI_2 + valve0_V_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_V_flow
]