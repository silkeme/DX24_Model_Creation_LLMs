import pandas as pd
from common import test_single_module, test_all_modules
from fdt_tests import conf
from fdt_tests.diag_tests import read_params

S2_conf = {
	'result_columns': conf.S2_result_columns,
	'files': conf.S2_files,
	'measurements': conf.S2_measurements,
	'mro': conf.S2_mro,
	'params': conf.S2_params
}


params = read_params(S2_conf['params'])
	
# Uncomment the following lines to test a single module
# module_name = 'results.Models.S2_3' # put full name of the module here
# test_single_module(module_name, params, S2_conf)
	
# Test all modules in the given range
module_numbers = list(range(1, 101)) # put the range of modules numbers here
name_prefix = 'results.Models.S2_' # put the prefix of the module name here
results_file_name = 'eval_results/S2_results.csv' # put the name of the results file here
test_all_modules(name_prefix, module_numbers, params, results_file_name, S2_conf)
