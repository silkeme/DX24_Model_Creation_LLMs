import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['der_tank1_m', 'der_tank1_V', 'der_tank1_level', 'tank1_cross_sectional_area'],
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pipe_Diameter', 'pipe4_Diameter', 'tank1_Diameter', 'pipe1_Diameter', 'pipe2_Diameter', 'pipe_Length', 'pipe4_Length', 'pipe1_Length', 'pipe2_Length', 'tank1_Height', 'pump_N_Nominal', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal', 'valve1_dp_nominal', 'pump_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Additional variables that are not in the lists but are used in the equations
sym.var('valve0_dp valve1_dp')

model_def['rels'] = [
    # Pump flow equation
    -FI_1 + pump_N * pump_V * (1 - f_pumpSlow),
    
    # Valve0 flow equation
    -FI_2 + valve0_opening * valve0_Flow_Nominal * sym.sqrt(1 - (valve0_dp / valve0_dp_nominal)**2) * (1 - f_valve0),
    
    # Valve1 flow equation
    -FI_4 + valve1_opening * valve1_Flow_Nominal * sym.sqrt(1 - (valve1_dp / valve1_dp_nominal)**2) * (1 - f_valve1),
    
    # Mass balance equation for tank1
    -der_tank1_m + valve0_flow - valve1_flow - f_tank1leak,
    
    # Volume balance equation for tank1
    -der_tank1_V + der_tank1_m / 1000,
    
    # Cross-sectional area of tank1
    -tank1_cross_sectional_area + (tank1_Diameter / 2)**2 * 3.14159,
    
    # Level change equation for tank1
    -der_tank1_level + der_tank1_V / tank1_cross_sectional_area,
    
    # Sensor equations
    -FI_1 + pump_flow,
    -FI_2 + valve0_flow,
    -LI_3 + der_tank1_level,
    -FI_4 + valve1_flow,
    
    # Differential equations
    fdt.DiffConstraint('der_tank1_m', 'tank1_m'),
    fdt.DiffConstraint('der_tank1_V', 'tank1_V'),
    fdt.DiffConstraint('der_tank1_level', 'tank1_level')
]

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If they do not occur in any of the mentioned lists, add them under key 'x'
additional_vars = ['valve0_dp', 'valve1_dp', 'tank1_m', 'tank1_V', 'tank1_level']
for var in additional_vars:
    if var not in model_def['x'] + model_def['f'] + model_def['z'] + model_def['parameters']:
        model_def['x'].append(var)