import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['tank1_level', 'pump_dp_pump', 'tank1_ports_1__p', 'der_tank1_level'],  # unknown variables
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],  # faults
    'z': ['FI_1', 'FI_2', 'LI_3', 'FI_4', 'pump_N', 'valve0_opening', 'valve1_opening'],  # known variables
    'parameters': ['pipe_Diameter', 'pipe4_Diameter', 'tank1_Diameter', 'pipe1_Diameter', 'pipe2_Diameter',
                   'pipe_Length', 'pipe4_Length', 'pipe1_Length', 'pipe2_Length', 'tank1_Height',
                   'pump_N_Nominal', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal',
                   'valve1_dp_nominal', 'pump_V']  # parameters
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Sensor equations
    -FI_1 + pump_N * pump_V,
    -FI_2 + valve0_opening * valve0_Flow_Nominal * (pump_dp_pump / valve0_dp_nominal)**0.5,
    -LI_3 + tank1_level,
    -FI_4 + valve1_opening * valve1_Flow_Nominal * (tank1_ports_1__p / valve1_dp_nominal)**0.5,
    
    # Component equations with faults
    -pump_N * pump_V + pump_N * pump_V * (1 - f_pumpSlow),
    -valve0_opening * valve0_Flow_Nominal * (pump_dp_pump / valve0_dp_nominal)**0.5 + valve0_opening * valve0_Flow_Nominal * (pump_dp_pump / valve0_dp_nominal)**0.5 * (1 - f_valve0),
    -valve1_opening * valve1_Flow_Nominal * (tank1_ports_1__p / valve1_dp_nominal)**0.5 + valve1_opening * valve1_Flow_Nominal * (tank1_ports_1__p / valve1_dp_nominal)**0.5 * (1 - f_valve1),
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_opening * valve0_Flow_Nominal * (pump_dp_pump / valve0_dp_nominal)**0.5 * (1 - f_valve0) - valve1_opening * valve1_Flow_Nominal * (tank1_ports_1__p / valve1_dp_nominal)**0.5 * (1 - f_valve1) - f_tank1leak) / (tank1_Diameter**2 * 3.14159 / 4)
]

# Output the complete model
print(model_def)