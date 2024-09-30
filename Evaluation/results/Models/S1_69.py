import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt
from sympy import sqrt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_dp_pump', 'tank1_ports_1__p', 'der_tank1_level', 'tank1_level'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pi', 'pump_N_Nominal', 'pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Pump equation
    -FI_1 + pump_N / pump_N_Nominal * pump_V * (1 - f_pumpSlow),
    
    # Valve equations
    -FI_2 + valve0_opening * valve0_Flow_Nominal * sqrt(pump_dp_pump / valve0_dp_nominal) * (1 - f_valve0),
    -FI_4 + valve1_opening * valve1_Flow_Nominal * sqrt(tank1_ports_1__p / valve1_dp_nominal) * (1 - f_valve1),
    
    # Tank mass balance
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (FI_2 - FI_4 - f_tank1leak) / (pi * (tank1_Diameter / 2)**2),
    
    # Sensor equations
    -LI_3 + tank1_level
]