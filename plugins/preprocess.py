#
# Preprocess plugin to prepare for a grid submission
# Victor E. Bazterra UIC (2012)
#

def parse_value(lit):
    'Return value of numeric literal string or ValueError exception'
    # Handle '0'
    if lit == '0': return 0
    # Hex/Binary
    litneg = lit[1:] if lit[0] == '-' else lit
    if litneg[0] == '0':
        if litneg[1] in 'xX':
            return int(lit,16)
        elif litneg[1] in 'bB':
            return int(lit,2)
        else:
            try:
                return int(lit,8)
            except ValueError:
                pass
    # Int/Float/Complex/String
    try:
        return int(lit)
    except ValueError:
        pass
    try:
        return float(lit)
    except ValueError:
        pass
    try:
        return complex(lit)
    except ValueError:
        pass
    if 'true' in lit.lower():
        return True
    elif 'false' in lit.lower():
        return False
    return lit


def parse_options(model):
    """ Parse model command line """
    global parse_value
    info = model.split(':')
    module = info[0]
    assert module != '', 'Syntax error no model name.'
    if len(info) == 1:
        return module, {}
    opts = info[1].split(',')
    args = {}
    for opt in opts:
        key = opt.split('=')[0].lstrip().rstrip()
        value = opt.split('=')[1].lstrip().rstrip()
        args[key] = parse_value(value)
    return module, args


from optparse import OptionParser

usage = 'usage: %prog postprocess [options] [file1] [file2] ...\n'
usage = usage + 'Prepare theta for grid submission.'

parser = OptionParser(
    usage = usage
)

parser.add_option(
    '--model', type='string',
    help='Input model and argments in the format "file: arg1 = val1, arg2 = val2, ..."'
)
parser.add_option(
    '--analysis', type='string', default='summary',
    help='Analysis to be done to the model [default: %default]."'
)
parser.add_option(
    '--workdir', type='string',
    help='Working directory of the driver."'
)
parser.add_option(
    '--remotedir', type='string',
    help='Remote directory to put all the produced theta files."'
)

(options, args) = parser.parse_args()

import os

if 'THETA_PATH' not in os.environ:
    raise EnvironmentError('Missing THETA_PATH environment variable, source setup first.')

import exceptions

if not options.workdir:
    raise exceptions.ValueError('Undefined working directory.') 

# Create working directory
if not os.path.exists(options.workdir):
    os.makedirs(options.workdir)

# Processing model information
model, model_opts = parse_options(options.model) 
analysis, analysis_opts = parse_options(options.analysis)

import shutil

# Copy the content of the model in 
shutil.copy(model+'.py', '%s/analysis.py' % options.workdir)

# Append the model file by adding the options and actions
file = open('%s/analysis.py' % options.workdir, 'a')
file.write('\n\n')
file.write('# Code introduced by theta_driver\n\n')
file.write('# Building the statistical model\n')
file.write('args = %s\n\n' % str(model_opts))
file.write('model = build_model(**args)\n\n')
if analysis == 'summary':
    file.write('model_summary(model)\n')
elif analysis == 'expected_asymptotic':
    file.write('limits = get_expected_pl_limits(model)\n')
    file.write("for sp in sorted(limits.keys()): print '%s %.4f' % (sp, limits[sp])\n")
elif analysis == 'observed_asymptotic':
    file.write('limits = get_observed_pl_limits(model)\n')
    file.write("for sp in sorted(limits.keys()): print '%s %.4f' % (sp, limits[sp])\n")
elif analysis == 'bayesian':
    file.write('args = %s\n\n' % str(analysis_opts))
    file.write('results = bayesian_limits(model, run_theta = False, **args)\n')
elif analysis == 'cls':
    file.write('args = %s\n\n' % str(analysis_opts))
    file.write("results = cls_limits(model, ts = 'lhclike', run_theta = False, write_debuglog = True, **args)\n")
file.close()

commands = []

# Link all the file dependency
files = []
for arg in args:
    if not os.path.isfile(arg): continue
    commands.append('ln -sf ../%s %s' % (arg, options.workdir))
    files.append(os.path.basename(arg))

# Execute theta to produce only cfg files
if os.path.exists('%s/analysis' % options.workdir):
    commands.append('cd %s; rm -rf analysis' % options.workdir)
commands.append('cd %s; %s/utils/theta-auto.py analysis.py' % (options.workdir, os.environ['THETA_PATH']))

if not options.analysis == 'summary' or not 'asymptotic' in options.analysis:
    commands = commands + [
        'cd %s; tar cz analysis/ > analysis.tgz' % options.workdir,
        'cp %s/utils/grid_theta_executable.* %s' % (os.environ['THETA_DRIVER_PATH'], options.workdir)
    ]

    if not os.path.isfile('%s/gridpack/gridpack.tgz' % os.environ['THETA_PATH']):
        commands.append('cd %s; ./build.sh' % os.environ['THETA_PATH'])
    commands.append('cp %s/gridpack/gridpack.tgz %s' % (os.environ['THETA_PATH'], options.workdir))

import subprocess
for command in commands:
    print command
    subprocess.call( [command], shell=True )

# Prepare crab cfg file

# This is only if a report is not issued
if options.analysis == 'summary':
    sys.exit(0)

# Reads how many cfg files are generated
njobs = 0
dir = os.listdir('%s/analysis' % options.workdir)
for file in dir:
    if '.cfg' in file: 
        njobs = njobs + 1

import string

if options.remotedir:
    file = open('%s/utils/grid_theta_crab_remotedir.cfg' % os.environ['THETA_DRIVER_PATH'])
    cfg = string.Template(file.read())
    file.close()
    cfg = cfg.safe_substitute(
        njobs = njobs, 
        user = os.environ['USER'],
        files = ','.join(files),
        remotedir = options.remotedir 
    )
else:
    file = open('%s/utils/grid_theta_crab_cacheddir.cfg' % os.environ['THETA_DRIVER_PATH'])
    cfg = string.Template(file.read())
    file.close()
    cfg = cfg.safe_substitute(
        njobs = njobs,
        user = os.environ['USER'],
        files = ','.join(files),
    )

file = open('%s/grid_theta_crab.cfg' % options.workdir, 'w')
file.write(cfg)
