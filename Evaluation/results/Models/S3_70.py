import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': ['valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow', 'valveLinear4_V_flow',
          'valveLinear5_V_flow', 'valveLinear6_V_flow', 'der_tank1_level', 'der_tank2_level', 'der_tank3_level',
          'der_tank4_level', 'tank1_A', 'tank2_A', 'tank3_A', 'tank4_A'],
    'f': ['f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'],
    'z': ['FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17',
          'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening', 'valveLinear4_opening',
          'valveLinear5_opening', 'valveLinear6_opening', 'valveLinear7_opening'],
    'parameters': ['pipe1_Length', 'pipe7_Length', 'pipe2_Length', 'pipe3_Length', 'pipe4_Length', 'pipe5_Length', 'pipe6_Length',
                   'pipe1_Diameter', 'pipe7_Diameter', 'pipe2_Diameter', 'pipe3_Diameter', 'pipe4_Diameter', 'pipe5_Diameter', 'pipe6_Diameter',
                   'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter', 'tank1_Height', 'tank2_Height', 'tank3_Height', 'tank4_Height',
                   'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'valveLinear4_Flow_Nominal',
                   'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal', 'valveLinear7_Flow_Nominal', 'valveLinear1_dp_nominal',
                   'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'valveLinear4_dp_nominal', 'valveLinear5_dp_nominal',
                   'valveLinear6_dp_nominal', 'valveLinear7_dp_nominal']
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

model_def['rels'] = [
    # Valve flow equations
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal,
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal,
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal,
    -valveLinear4_V_flow + valveLinear4_opening * valveLinear4_Flow_Nominal,
    -valveLinear5_V_flow + valveLinear5_opening * valveLinear5_Flow_Nominal,
    -valveLinear6_V_flow + valveLinear6_opening * valveLinear6_Flow_Nominal,
    
    # Tank area equations
    -tank1_A + (tank1_Diameter / 2) ** 2 * sym.pi,
    -tank2_A + (tank2_Diameter / 2) ** 2 * sym.pi,
    -tank3_A + (tank3_Diameter / 2) ** 2 * sym.pi,
    -tank4_A + (tank4_Diameter / 2) ** 2 * sym.pi,
    
    # Tank level derivative equations
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    fdt.DiffConstraint('der_tank3_level', 'tank3_level'),
    fdt.DiffConstraint('der_tank4_level', 'tank4_level'),
    
    -der_tank1_level + (valveLinear1_V_flow - valveLinear2_V_flow - valveLinear3_V_flow) / tank1_A,
    -der_tank2_level + (valveLinear2_V_flow - valveLinear4_V_flow) / tank2_A + f_tank2leak,
    -der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / tank3_A * (1 - f_valve3),
    -der_tank4_level + (valveLinear4_V_flow + valveLinear5_V_flow - valveLinear6_V_flow) / tank4_A * (1 - f_pipe4),
    
    # Sensor equations
    -FI_13 + valveLinear1_V_flow,
    -LI_21 + der_tank1_level,
    -FI_14 + valveLinear2_V_flow,
    -LI_22 + der_tank2_level,
    -FI_15 + valveLinear3_V_flow,
    -LI_23 + der_tank3_level,
    -FI_16 + valveLinear4_V_flow,
    -LI_24 + der_tank4_level,
    -FI_17 + valveLinear6_V_flow * (1 - f_valve6)
]

# Output the complete model
print(model_def)