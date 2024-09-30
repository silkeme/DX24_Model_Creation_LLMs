sim_beg_cutoff = 6
fault_start = 250
zero_thr = 0.1
causality = 'int'

# S1
S1_result_columns = ['Number of MSOs', 'Number of residual generators',
                     'Number of computed residuals', 'valve0 detected',
                     'tank1leak detected', 'ambiguity groups']

S1_files = ['../Examples/S1/Data/S1_valve0.csv', '../Examples/S1/Data/S1_tank1leak.csv']
S1_params = '../Examples/S1/S1_parameters.csv'

S1_measurements = {'FI_1': 'pump_V_flow', 'FI_2': 'valve0_V_flow', 'FI_4': 'valve1_V_flow',
                   'LI_3': 'tank1_level', 'FI1': 'pump_V_flow', 'FI2': 'valve0_V_flow',
                   'FI4': 'valve1_V_flow', 'LI3': 'tank1_level'}
S1_mro = {'tank1_level': ['LI3', 'LI_3']}


# S2
S2_result_columns = ['Number of MSOs', 'Number of residual generators',
                     'Number of computed residuals', 'tank1leak detected', 'tank2leak detected',
                     'ambiguity groups']

S2_files = ['../Examples/S2/Data/S2_tank1leak.csv', '../Examples/S2/Data/S2_tank2leak.csv']
S2_params = '../Examples/S2/S2_parameters.csv'

S2_measurements = {'FI1': 'pump_V_flow', 'LI2': 'tank1_level', 'FI3': 'valveLinear1_V_flow', 'LI4': 'tank_level',
                   'FI5': 'pump1_V_flow', 'LI6': 'tank2_level', 'FI7': 'valveLinear3_V_flow',
                   'FI_1': 'pump_V_flow', 'LI_2': 'tank1_level', 'FI_3': 'valveLinear1_V_flow', 'LI_4': 'tank_level',
                   'FI_5': 'pump1_V_flow', 'LI_6': 'tank2_level', 'FI_7': 'valveLinear3_V_flow'}

S2_mro = {'tank1_level': ['LI2', 'LI_2'], 'tank2_level': ['LI6', 'LI_6']}

# S3
S3_result_columns = ['Number of MSOs', 'Number of residual generators',
                     'Number of computed residuals', 'pipe4 detected', 'tank2leak detected',
                     'valve3 detected', 'valve6 detected', 'ambiguity groups']

S3_files = ['../Examples/S3/Data/S3_pipe4.csv', '../Examples/S3/Data/S3_tank2leak.csv', '../Examples/S3/Data/S3_valve3.csv', '../Examples/S3/Data/S3_valve6.csv']
S3_params = '../Examples/S3/S3_parameters.csv'

S3_measurements = {'FI_13': 'valveLinear1_V_flow', 'LI_21': 'tank1_level', 'FI_14': 'valveLinear2_V_flow',
                   'FI_15': 'valveLinear7_V_flow', 'LI_22': 'tank2_level', 'LI_23': 'tank3_level', 
                   'FI_16': 'valveLinear5_V_flow', 'LI_24': 'tank4_level', 'FI_17': 'valveLinear6_V_flow',
                   'FI13': 'valveLinear1_V_flow', 'LI21': 'tank1_level', 'FI14': 'valveLinear2_V_flow',
                   'FI15': 'valveLinear7_V_flow', 'LI22': 'tank2_level', 'LI23': 'tank3_level', 
                   'FI16': 'valveLinear5_V_flow', 'LI24': 'tank4_level', 'FI17': 'valveLinear6_V_flow'}
S3_mro = {'tank1_level': ['LI21', 'LI_21'], 'tank2_level': ['LI22', 'LI_22'], 'tank3_level': ['LI23', 'LI_23'],
            'tank4_level': ['LI24', 'LI_24']}
