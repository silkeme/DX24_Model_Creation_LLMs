import sympy as sym
import faultdiagnosistoolbox as fdt
import matplotlib.pyplot as plt

model_def = {
    'type': 'Symbolic',
    'x': [
        'der_tank1_level', 'tank1_V', 'valveLinear1_V_flow', 'valveLinear2_V_flow', 'valveLinear3_V_flow',
        'der_tank2_level', 'tank2_V', 'valveLinear4_V_flow',
        'der_tank3_level', 'tank3_V', 'valveLinear5_V_flow',
        'der_tank4_level', 'tank4_V', 'valveLinear6_V_flow',
        'valveLinear1_dp', 'valveLinear2_dp', 'valveLinear3_dp', 'valveLinear4_dp', 'valveLinear5_dp', 'valveLinear6_dp',
        'tank1_ports_2__p', 'tank2_ports_2__p', 'tank3_ports_2__p', 'tank4_ports_4__p', 'sink_p_in_internal',
        'tank1_medium_p', 'tank2_medium_p', 'tank3_medium_p', 'tank4_medium_p',
        'tank1_level', 'tank2_level', 'tank3_level', 'tank4_level'
    ],
    'f': [
        'f_tank2leak', 'f_pipe4', 'f_valve3', 'f_valve6'
    ],
    'z': [
        'FI_13', 'LI_21', 'FI_14', 'LI_22', 'FI_15', 'LI_23', 'FI_16', 'LI_24', 'FI_17',
        'valveLinear1_opening', 'valveLinear2_opening', 'valveLinear3_opening', 'valveLinear4_opening', 'valveLinear5_opening', 'valveLinear6_opening'
    ],
    'parameters': [
        'pipe1_Length', 'pipe7_Length', 'pipe2_Length', 'pipe3_Length', 'pipe4_Length', 'pipe5_Length', 'pipe6_Length',
        'pipe1_Diameter', 'pipe7_Diameter', 'pipe2_Diameter', 'pipe3_Diameter', 'pipe4_Diameter', 'pipe5_Diameter', 'pipe6_Diameter',
        'tank1_Diameter', 'tank2_Diameter', 'tank3_Diameter', 'tank4_Diameter',
        'tank1_Height', 'tank2_Height', 'tank3_Height', 'tank4_Height',
        'valveLinear1_Flow_Nominal', 'valveLinear2_Flow_Nominal', 'valveLinear3_Flow_Nominal', 'valveLinear4_Flow_Nominal', 'valveLinear5_Flow_Nominal', 'valveLinear6_Flow_Nominal',
        'valveLinear1_dp_nominal', 'valveLinear2_dp_nominal', 'valveLinear3_dp_nominal', 'valveLinear4_dp_nominal', 'valveLinear5_dp_nominal', 'valveLinear6_dp_nominal'
    ],
    'rels': []
}

sym.var(model_def['x'])
sym.var(model_def['f'])
sym.var(model_def['z'])
sym.var(model_def['parameters'])

# Tank level dynamics (continuity equation)
model_def['rels'].append(-der_tank1_level + (FI_13 - valveLinear2_V_flow - valveLinear3_V_flow) / tank1_V)
model_def['rels'].append(-der_tank2_level + (FI_14 - valveLinear4_V_flow) / tank2_V - f_tank2leak)
model_def['rels'].append(-der_tank3_level + (FI_15 - valveLinear5_V_flow) / tank3_V)
model_def['rels'].append(-der_tank4_level + (valveLinear4_V_flow + valveLinear5_V_flow - FI_17) / tank4_V)

# Valve flow equations (assuming linear valve characteristics)
model_def['rels'].append(-valveLinear1_V_flow + valveLinear1_Flow_Nominal * valveLinear1_opening * (1 - (valveLinear1_dp / valveLinear1_dp_nominal)))
model_def['rels'].append(-valveLinear2_V_flow + valveLinear2_Flow_Nominal * valveLinear2_opening * (1 - (valveLinear2_dp / valveLinear2_dp_nominal)))
model_def['rels'].append(-valveLinear3_V_flow + valveLinear3_Flow_Nominal * valveLinear3_opening * (1 - (valveLinear3_dp / valveLinear3_dp_nominal)) * (1 - f_valve3))
model_def['rels'].append(-valveLinear4_V_flow + valveLinear4_Flow_Nominal * valveLinear4_opening * (1 - (valveLinear4_dp / valveLinear4_dp_nominal)) * (1 - f_pipe4))
model_def['rels'].append(-valveLinear5_V_flow + valveLinear5_Flow_Nominal * valveLinear5_opening * (1 - (valveLinear5_dp / valveLinear5_dp_nominal)))
model_def['rels'].append(-valveLinear6_V_flow + valveLinear6_Flow_Nominal * valveLinear6_opening * (1 - (valveLinear6_dp / valveLinear6_dp_nominal)) * (1 - f_valve6))

# Pressure drop across valves (hydrostatic pressure difference)
model_def['rels'].append(-valveLinear1_dp + tank1_ports_2__p - tank1_ports_2__p)
model_def['rels'].append(-valveLinear2_dp + tank1_ports_2__p - tank2_ports_2__p)
model_def['rels'].append(-valveLinear3_dp + tank1_ports_2__p - tank3_ports_2__p)
model_def['rels'].append(-valveLinear4_dp + tank2_ports_2__p - tank4_ports_4__p)
model_def['rels'].append(-valveLinear5_dp + tank3_ports_2__p - tank4_ports_4__p)
model_def['rels'].append(-valveLinear6_dp + tank4_ports_4__p - sink_p_in_internal)

# Tank pressures (assuming open tanks at atmospheric pressure)
model_def['rels'].append(-tank1_medium_p + tank1_ports_2__p)
model_def['rels'].append(-tank2_medium_p + tank2_ports_2__p)
model_def['rels'].append(-tank3_medium_p + tank3_ports_2__p)
model_def['rels'].append(-tank4_medium_p + tank4_ports_4__p)

# Tank heights (from level sensors)
model_def['rels'].append(-tank1_level + LI_21)
model_def['rels'].append(-tank2_level + LI_22)
model_def['rels'].append(-tank3_level + LI_23)
model_def['rels'].append(-tank4_level + LI_24)

# Differential equations
model_def['rels'].append(fdt.DiffConstraint('der_tank1_level', 'tank1_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank2_level', 'tank2_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank3_level', 'tank3_level'))
model_def['rels'].append(fdt.DiffConstraint('der_tank4_level', 'tank4_level'))