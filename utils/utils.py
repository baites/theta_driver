
def limit_table(exp, obs):
    file = open('limits.yaml', 'w')
    for i in range(len(exp.x)):
        file.write(
            '%.2f: [%.6f, %.6f, %.6f, %.6f, %.6f, %.6f]\n' % (
                exp.x[i], exp.y[i],
                exp.bands[1][1][i] - exp.y[i], exp.bands[1][0][i] - exp.y[i],
                exp.bands[0][1][i] - exp.y[i], exp.bands[0][0][i] - exp.y[i],
                obs.y[i]
            )
        )


def apply_factors(model, factors):
    for obs in factors:
        for proc in factors[obs]:
            f = factors[obs][proc]
            if type(f) == str: continue # can happen for "n/a"
            model.scale_predictions(f, proc, obs)


def generate_yield_table(rate_table):
    rows = rate_table.get_raw_rows()
    cols = rate_table.get_columns()
    f = open('yield-table.tex', 'w')
    f.write('\\begin{tabular}{|l|')
    for c in cols: f.write('r|')
    f.write('}\n \\hline\n Process')
    for c in cols:
        if c=='process': continue
        latex_colname = {'el_0btag_mttbar': 'electron channel, $N_{\\text{b-tag}}=0$',
                         'el_1btag_mttbar': 'electron channel, $N_{\\text{b-tag}} \\ge 1$',
                         'mu_0btag_mttbar': 'muon channel, $N_{\\text{b-tag}}=0$',
                         'mu_1btag_mttbar': 'muon channel, $N_{\\text{b-tag}} \\ge 1$'}[c]
        f.write('& %s' % latex_colname)
    f.write('\\\\\n')
    for r in rows:
        f.write('%10s' % r[0])
        for val in r[1:]:
            if type(val)==tuple: val = val[0]
            if type(val)==float: f.write(' & %6.1f' % val)
            else: f.write(' & %10s' % val)
        f.write('\\\\ \n')
    f.write('\\\\ \n \\hline')
    f.write('\\end{tabular}\n')


def print_obsproc_factors_shapes(model):
    result = {}
    res = ml_fit2(model, signal_processes = [''], nuisance_constraint = '')
    par_values = {}
    par_values0 = {}
    for par in model.get_parameters(''):
        par_values[par] = res[''][par][0][0]
        par_values0[par] = 0.0 # assuming 0.0 means "nominal"
    for p in par_values: print p, par_values[p]
    templates0 = get_shifted_templates(model, par_values0, False)
    templates = get_shifted_templates(model, par_values, False)
    for obs in templates:
        print("\n" + obs)
        result[obs] = {}
        for proc in templates[obs]:
            nominal_rate = sum(templates0[obs][proc][2])
            if nominal_rate == 0.0: factor = "n/a (%f / %f)" % (sum(templates[obs][proc][2]), nominal_rate)
            else: factor = sum(templates[obs][proc][2]) / nominal_rate
            print "  ", proc, factor
            result[obs][proc] = factor
    return result


def print_obsproc_factors_rateonly(model):
    result = {}
    res = ml_fit_coefficients(model, signal_processes = [''])
    for obs in res['']:
        print("\n" + obs)
        result[obs] = {}
        for proc in res[''][obs]:
            print "  ", proc, res[''][obs][proc]
            result[obs][proc] = res[''][obs][proc]
    return result


