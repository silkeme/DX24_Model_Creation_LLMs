import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'valve0_flow', 'valve1_flow', 'der_tank1_level', 'valve0_dp', 'valve1_dp', 'tank1_ports_1__p', 'tank1_ports_2__p', 'tank1_level', 'pump_dp_pump'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations
    -pump_flow + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - (valve0_dp / valve0_dp_nominal)**2)**0.5 * (1 - f_valve0),
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - (valve1_dp / valve1_dp_nominal)**2)**0.5 * (1 - f_valve1),
    -der_tank1_level + (valve0_flow - valve1_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2)**2),
    -valve0_dp + pump_dp_pump,
    -valve1_dp + tank1_ports_1__p - tank1_ports_2__p,
    -tank1_ports_2__p + 0,
    
    # Sensor equations
    -FI_1 + pump_flow,
    -FI_2 + valve0_flow,
    -LI_3 + tank1_level,
    -FI_4 + valve1_flow,
    
    # Differential equations
    fdt.DiffConstraint('der_tank1_level', 'tank1_level')
]