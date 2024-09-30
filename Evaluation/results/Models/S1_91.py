import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'valve0_flow', 'valve1_flow', 'der_tank1_level', 'tank1_cross_sectional_area'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_N_Nominal', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'tank1_Diameter', 'pump_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations
    -pump_flow + pump_N / pump_N_Nominal * pump_V * (1 - f_pumpSlow),
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - f_valve0),
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - f_valve1),
    -tank1_cross_sectional_area + (tank1_Diameter / 2) ** 2 * 3.14159,
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),  # Assuming 'tank1_level' is the variable to be differentiated
    -(der_tank1_level) + (valve0_flow - valve1_flow - f_tank1leak) / tank1_cross_sectional_area,
    
    # Sensor equations
    -FI_1 + pump_flow,
    -FI_2 + valve0_flow,
    -LI_3 + der_tank1_level,
    -FI_4 + valve1_flow
]

# Assuming 'tank1_level' is a state variable that was not included in the original 'x' list
model_def['x'].append('tank1_level')