import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'der_tank1_level', 'der_tank2_level', 'der_tank3_level', 'der_tank4_level',
        'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
        'valveLinear4_V_flow', 'valveLinear5_V_flow', 'valveLinear6_V_flow',
        'tank1_level', 'tank2_level', 'tank3_level', 'tank4_level'  # Added missing tank level variables
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
        'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter',
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal',
        'valveLinear3_Flow_Nominal', 'valveLinear4_Flow_Nominal',
        'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal',
        'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal',
        'valveLinear3_dp_nominal', 'valveLinear4_dp_nominal',
        'valveLinear5_dp_nominal', 'valveLinear6_dp_nominal'
    ],
    'rels': []
}

# Create symbolic variables
sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Define the equations and add them to the 'rels' list
model_def['rels'].extend([
    # Tank level dynamics (continuity equation)
    -der_tank1_level + (FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / (sym.pi * (tank1_Diameter / 2) ** 2),
    -der_tank2_level + (FI_14 - valveLinear4_V_flow) / (sym.pi * (tank2_Diameter / 2) ** 2) - f_tank2leak,
    -der_tank3_level + (FI_15 - valveLinear5_V_flow) / (sym.pi * (tank3_Diameter / 2) ** 2),
    -der_tank4_level + (FI_16 + valveLinear5_V_flow - FI_17) / (sym.pi * (tank4_Diameter / 2) ** 2) - f_pipe4,
    
    # Valve flow dynamics (assuming linear valve characteristics)
    -valveLinear1_V_flow + valveLinear1_opening * valveLinear1_Flow_Nominal,
    -valveLinear2_V_flow + valveLinear2_opening * valveLinear2_Flow_Nominal,
    -valveLinear3_V_flow + valveLinear3_opening * valveLinear3_Flow_Nominal * (1 - f_valve3),
    -valveLinear4_V_flow + valveLinear4_opening * valveLinear4_Flow_Nominal,
    -valveLinear5_V_flow + valveLinear5_opening * valveLinear5_Flow_Nominal,
    -valveLinear6_V_flow + valveLinear6_opening * valveLinear6_Flow_Nominal * (1 - f_valve6),
    
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

# Add differential constraints for the tank level derivatives
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank3_level', 'tank3_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank4_level', 'tank4_level'))

# Check if all variables in the equations occur in any of the lists 'x', 'f', 'z' or 'parameters'
# If not, add them under key 'x'
# (This step is not needed as all variables are already accounted for in the lists)

# The model is now ready to be used with the faultdiagnosis toolbox