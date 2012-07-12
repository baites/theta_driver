#
# Postprocess plugin to run theta after generating toys on grid
# Victor E. Bazterra UIC (2012)
#

from optparse import OptionParser

parser = OptionParser(
    usage = 'usage: %prog postprocess [options]'
)

parser.add_option(
    '--workdir', type='string',
    help='Working directory of the driver."'
)

(options, args) = parser.parse_args()

import shutil

# Append the model file by adding the options and actions

commands = [
    'cd %s; cp analysis/*.cfg analysis/cache',
    "cd %s; sed -e 's/run_theta = False/run_theta = True/' analysis.py > tmp.py; mv tmp.py analysis.py" % options.workdir,
    'cd %s; %s/utils/theta-auto.py analysis.py' % (options.workdir, os.environ['THETA_PATH'])
]

import subprocess
for command in commands:
    print command
    subprocess.call( [command], shell=True )

