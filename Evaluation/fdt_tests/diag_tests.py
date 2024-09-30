import faultdiagnosistoolbox as fdt
import sympy as sym
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import importlib
import seaborn as sns
import os

from fdt_tests import conf

sns.set_style("whitegrid")

def read_params(params_file):
    params_df = pd.read_csv(params_file, sep=';')
    params = dict(zip(params_df['Parameter'].str.replace('.', '_'), params_df['Value']))
    return params

def read_file(file_name, measurements):
    df = pd.read_csv(file_name)
    cols_map = {c: c.replace('.', '_').replace('(', '_').replace(')', '') for c in df.columns}
    df.rename(columns=cols_map, inplace=True)

    for key, value in measurements.items():
        df[key] = df[value]
    
    return df

def generate_residuals(model, msos):
    res_gen_names = []
    for k, M in enumerate(msos):
        try:
            res_gen_name = 'ResGen' + str(k)
            cs = model.MSOCausalitySweep(M)
            if 'int' in cs:
                index = cs.index('int')
            elif 'algebraic' in cs:
                index = cs.index('algebraic')
            else:
                index = 0
            r = M[index]
            M0 = [e for e in M if e != r]
            Gamma = model.Matching(M0)
            file_path = res_gen_name + '.py'
            if os.path.exists(file_path):
                os.remove(file_path)
            model.SeqResGen(Gamma, r, res_gen_name)
            res_gen_names.append(res_gen_name)
        except Exception as e:
            print('Residual generation: ', res_gen_name, e)
            file_path = res_gen_name + '.py'
            if os.path.exists(file_path):
                os.remove(file_path)
            
    return res_gen_names

def _compute_residual(file_name, ResGen, model_def, measurements, params, mro_vars):
    df = read_file(file_name, measurements)
    dat = df[conf.sim_beg_cutoff:].reset_index()
    r = np.zeros(len(dat)) 
    z = dat[model_def['z']]
    state = {x: dat[x].iloc[0] if x in dat.columns else 0 for x in model_def['x']}
    for k, zk in enumerate(z.itertuples()):
        r[k], state = ResGen(zk[1:], state, params, 1)
        mro(model_def, state, zk, mro_vars)

    del state
    del df
    del dat
    del z
    return r

def mro(model_def, state, zk, mro_vars, alpha=0.1):
    for key in mro_vars.keys():
        if key in state:
            for sensor in mro_vars[key]:
                if sensor in model_def['z']:
                    state[key] = (1 - alpha) * state[key] + alpha * zk[model_def['z'].index(sensor) + 1]
                    break

def compute_residuals(res_gen_names, files, model_def, measurements, params, mro_vars):
    res = {}
    n_comp_residuals = 0
    for res_gen_name in res_gen_names:
        module = importlib.import_module(res_gen_name)
        importlib.reload(module)
        ResGen = getattr(module, res_gen_name)
        for file_name in files:
            try:
                r = _compute_residual(file_name, ResGen, model_def, measurements, params, mro_vars)
                n_comp_residuals += 1
                res[(res_gen_name, file_name)] = r
            except Exception as e:
                print('Residual computation', res_gen_name, file_name, e)
        del module
    return res, n_comp_residuals/len(files)

def make_plots(res, files, res_gen_names, module_name):
    if len(res_gen_names) > 20:
        return
    fig, axs = plt.subplots(len(files), len(res_gen_names), figsize=(1.3 * len(res_gen_names), 1.15 * len(files)), sharex=True)
    if len(res_gen_names) > 1:
        for col in range(len(res_gen_names)):
            for row in range(len(files)):
                axs[row, col].sharey(axs[0, col])

    for j, res_gen_name in enumerate(res_gen_names):
        for k, file_name in enumerate(files):
            if (res_gen_name, file_name) in res:
                if len(res_gen_names) == 1:
                    ax = axs[k]
                else:
                    ax = axs[k, j]
                ax.plot(res[(res_gen_name, file_name)])
                if k == 0:
                    ax.set_xlabel(res_gen_name)
                    ax.xaxis.set_label_position('top') 
                if j == 0:
                    ax.set_ylabel(file_name.rstrip('.csv'))
                    
    plt.tight_layout()
    plt.savefig('eval_results/eval_pic/' + module_name.lstrip('results.') + '.pdf')

def get_fsm(res, files, res_gen_names):
    fsm = []
    for file_name in files:
        fault_signature = []
        for res_gen_name in res_gen_names:
            det = 0
            if (res_gen_name, file_name) in res:
                r = res[(res_gen_name, file_name)]
                fault_start = conf.fault_start - conf.sim_beg_cutoff
                r_nf = np.abs(r[:fault_start])
                r_f = np.abs(r[fault_start:])
                if (r_nf.std() < 0.2 or r_nf.mean() < conf.zero_thr) and (r_nf.mean() + 2 * r_nf.std() + conf.zero_thr < r_f.mean()):
                    det = 1

            fault_signature.append(det)
        fsm.append(fault_signature)
    return fsm

def evaluate_fsm(fsm, files):
    names = [f.split('/')[-1].rstrip('.csv') for f in files] + ['NF']
    fsm = np.array(fsm)
    if len(fsm[0]) == 0:
        det = np.zeros(len(files))
    else:
        det = fsm.max(axis=1)
    fsm = np.vstack((fsm, np.zeros((1, fsm.shape[1]))))
    ambiguity_groups= {}
    for idx, col in enumerate(fsm):
        col_tuple = tuple(col)
        if col_tuple in ambiguity_groups:
            ambiguity_groups[col_tuple].add(names[idx])
        else:
            ambiguity_groups[col_tuple] = {names[idx]}

    ambiguity_groups = [names for names in ambiguity_groups.values()]

    return det, ambiguity_groups

def test_module(module_name, files, measurements, params, mro_vars, make_plots=False):
    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        print('module import: ', module_name, e)
        return

    model_def = module.model_def
    model = fdt.DiagnosisModel(model_def)
    msos = model.MSO()
    msos = [m for m in msos if model.IsLowIndex(m)]
    if conf.causality == 'int':
        msos_filt = []
        for m in msos:
            try:
                cs = model.MSOCausalitySweep(m)
                if 'int' in cs or 'algebraic' in cs:
                    msos_filt.append(m)
            except Exception as e:
                print('Causality sweep: ', m, e)
        msos = msos_filt
    n_mso = len(msos)
    res_gen_names = generate_residuals(model, msos)
    n_gen_residuals = len(res_gen_names)
    res, n_comp_residuals = compute_residuals(res_gen_names, files, model_def, measurements, params, mro_vars)
    if make_plots and n_comp_residuals > 0:
        make_plots(res, files, res_gen_names, module_name)
    fsm = get_fsm(res, files, res_gen_names)
    det, ambiguity_groups = evaluate_fsm(fsm, files)

    for file in res_gen_names:
        try:
                os.remove(file + '.py')
        except Exception as e:
                print("Error deleting file:", file, e)

    return n_mso, n_gen_residuals, n_comp_residuals, *det, ambiguity_groups

def test_modules(module_name_prefix, module_numbers, files, measurments, params, mro_vars):
    n_import_errors = 0
    results = dict()
    for j in module_numbers:
        module_name = module_name_prefix + str(j)
        print('-------------------' + module_name + '---------------------------')

        module_result = test_module(module_name, files, measurments, params, mro_vars)
        if module_result is not None:
            results[module_name.lstrip('results.')] = module_result
        else:
            n_import_errors += 1

    print("Number of import errors: ", n_import_errors)
    return results