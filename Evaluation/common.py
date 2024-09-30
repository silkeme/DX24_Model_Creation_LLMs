import pandas as pd
from fdt_tests.diag_tests import test_module, test_modules, read_params

def test_single_module(module_name, params, conf):
    """Test a single module and print the results."""
    test_res = test_module(module_name, conf['files'], conf['measurements'], params, mro_vars=conf['mro'], make_plots=True)
    print(list(zip(conf['result_columns'], test_res)))

def test_all_modules(name_prefix, module_numbers, params, results_file_name, conf):
    """Test all modules in the given range and save the results to a CSV file."""
    results = test_modules(name_prefix, module_numbers, conf['files'], conf['measurements'], params, conf['mro'])
    results_df = pd.DataFrame(results).transpose()
    results_df = results_df.set_axis(conf['result_columns'], axis=1)
    results_df.to_csv(results_file_name, sep=';')