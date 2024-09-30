import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow', 'valveLinear4_V_flow', 
        'valveLinear5_V_flow', 'valveLinear6_V_flow', 'der_tank1_level', 'der_tank2_level', 
        'der_tank3_level', 'der_tank4_level', 'valveLinear1_dp', 'valveLinear2_dp', 
        'valveLinear3_dp', 'valveLinear4_dp', 'valveLinear5_dp', 'valveLinear6_dp',
        'tank1_Area', 'tank2_Area', 'tank3_Area', 'tank4_Area', 'tank1_level', 'tank2_level', 
        'tank3_level', 'tank4_level', 'pi'
    ],
    'f': [
        'f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'
    ],
    'z': [
        'FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17',
        'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening', 
        'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'
    ],
    'parameters': [
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 
        'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal', 
        'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 
        'valveLinear4_dp_nominal', 'valveLinear5_dp_nominal', 'valveLinear6_dp_nominal', 
        'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter', 
        'tank1_Height', 'tank2_Height', 'tank3_Height', 'tank4_Height'
    ],
    'rels': []
}

# Create symbolic variables
sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Define pi as a symbolic constant
pi = sym.pi

# Add equations to the 'rels' list
model_def['rels'].extend([
    # Valve flow equations
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal * sym.sqrt(valveLinear1_dp / valveLinear1_dp_nominal),
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal * sym.sqrt(valveLinear2_dp / valveLinear2_dp_nominal),
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * sym.sqrt(valveLinear3_dp / valveLinear3_dp_nominal) * (1 - f_valve3),
    -valveLinear4_V_flow + valveLinear4_opening * valveLinear4_Flow_Nominal * sym.sqrt(valveLinear4_dp / valveLinear4_dp_nominal) * (1 - f_pipe4),
    -valveLinear5_V_flow + valveLinear5_opening * valveLinear5_Flow_Nominal * sym.sqrt(valveLinear5_dp / valveLinear5_dp_nominal),
    -valveLinear6_V_flow + valveLinear6_opening * valveLinear6_Flow_Nominal * sym.sqrt(valveLinear6_dp / valveLinear6_dp_nominal) * (1 - f_valve6),
    
    # Tank area equations
    -tank1_Area + (tank1_Diameter / 2) ** 2 * pi,
    -tank2_Area + (tank2_Diameter / 2) ** 2 * pi,
    -tank3_Area + (tank3_Diameter / 2) ** 2 * pi,
    -tank4_Area + (tank4_Diameter / 2) ** 2 * pi,
    
    # Differential equations for tank levels
    fdt.DiffConstraint('der_tank1_level', 'tank1_level'),
    fdt.DiffConstraint('der_tank2_level', 'tank2_level'),
    fdt.DiffConstraint('der_tank3_level', 'tank3_level'),
    fdt.DiffConstraint('der_tank4_level', 'tank4_level'),
    
    # Tank level derivative equations
    -der_tank1_level + (FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / tank1_Area,
    -der_tank2_level + (valveLinear2_V_flow - valveLinear4_V_flow) / tank2_Area - f_tank2leak,
    -der_tank3_level + (valveLinear3_V_flow - valveLinear5_V_flow) / tank3_Area,
    -der_tank4_level + (valveLinear4_V_flow + valveLinear5_V_flow - FI_17) / tank4_Area,
    
    # Sensor equations
    -FI_13 + valveLinear1_V_flow,
    -LI_21 + tank1_level,
    -FI_14 + valveLinear2_V_flow,
    -LI_22 + tank2_level,
    -FI_15 + valveLinear3_V_flow,
    -LI_23 + tank3_level,
    -FI_16 + valveLinear4_V_flow,
    -LI_24 + tank4_level,
    -FI_17 + valveLinear6_V_flow
])