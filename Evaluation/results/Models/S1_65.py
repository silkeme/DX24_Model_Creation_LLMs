import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['pump_flow', 'valve0_flow', 'der_tank1_level', 'valve1_flow', 'tank1_level',
          'der_pump_medium_T', 'der_pump_medium_p', 'der_tank1_medium_T', 'der_pipe4_flowModel_states_1__h',
          'der_pump_U', 'der_pump_m', 'der_pump_medium_u', 'der_pump_rho', 'der_tank1_U', 'der_tank1_V',
          'der_tank1_heatTransfer_states_1__d', 'der_tank1_m', 'der_tank1_medium_u', 'der_tank1_ports_1__h_outflow',
          'valve0_dp', 'valve1_dp'],  # Added missing variables
    'f': ['f_tank1leak', 'f_valve0', 'f_valve1', 'f_pumpSlow'],
    'z': ['FI1', 'FI2', 'LI3', 'FI4', 'pump_N', 'valve0_opening', 'valve1_opening'],
    'parameters': ['pipe_Diameter', 'pipe4_Diameter', 'tank1_Diameter', 'pipe1_Diameter', 'pipe2_Diameter',
                   'pipe_Length', 'pipe4_Length', 'pipe1_Length', 'pipe2_Length', 'tank1_Height',
                   'pump_N_Nominal', 'valve0_Flow_Nominal', 'valve1_Flow_Nominal', 'valve0_dp_nominal',
                   'valve1_dp_nominal', 'pump_V']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Equations for the pump
    -pump_flow + pump_N * pump_V * (1 - f_pumpSlow),
    
    # Equations for valve0
    -valve0_flow + valve0_opening * valve0_Flow_Nominal * (1 - (valve0_dp / valve0_dp_nominal)**2) * (1 - f_valve0),
    
    # Equations for tank1
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    -der_tank1_level + (valve0_flow - valve1_flow) / (sym.pi * (tank1_Diameter / 2)**2) - f_tank1leak,
    -tank1_level + LI3,
    
    # Equations for valve1
    -valve1_flow + valve1_opening * valve1_Flow_Nominal * (1 - (valve1_dp / valve1_dp_nominal)**2) * (1 - f_valve1),
    
    # Sensor equations
    -FI1 + pump_flow,
    -FI2 + valve0_flow,
    -FI4 + valve1_flow
]