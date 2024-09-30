import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valve0_dp', 'valve1_dp', 'tank1_level', 'der_tank1_level', 'pump_V_flow', 'valve0_V_flow', 'valve1_V_flow', 'tank1_ports_2__m_flow'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pump_V', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'tank1_Diameter']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Pump equation
    -pump_V_flow + pump_N * pump_V * (1 - f_pumpSlow),
    
    # Valve flow equations
    -valve0_V_flow + valve0_opening * valve0_Flow_Nominal * sym.sqrt(1 - (valve0_dp / valve0_dp_nominal)**2) * (1 - f_valve0),
    -valve1_V_flow + valve1_opening * valve1_Flow_Nominal * sym.sqrt(1 - (valve1_dp / valve1_dp_nominal)**2) * (1 - f_valve1),
    
    # Tank level equation
    -der_tank1_level + (valve0_V_flow - valve1_V_flow - f_tank1leak) / (sym.pi * (tank1_Diameter / 2)**2),
    
    # Tank outflow equation
    -tank1_ports_2__m_flow + valve1_V_flow,
    
    # Sensor equations
    -FI1 + pump_V_flow,
    -FI2 + valve0_V_flow,
    -LI3 + tank1_level,
    -FI4 + valve1_V_flow,
    
    # Differential equation for tank level
    fdt.DiffConstraint('der_tank1_level', 'tank1_level')
]