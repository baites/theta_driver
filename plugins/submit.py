#
# Submit plugin to for submitting jobs to the grid
# Victor E. Bazterra UIC (2012)
#

from optparse import OptionParser

parser = OptionParser(
    usage = 'usage: %prog preprocess [options] [file1] [file2] ...'
)

parser.add_option(
    '--workdir', type='string',
    help='Working directory of the driver."'
)

(options, args) = parser.parse_args()

commands = [
    'cd %s; crab -USER.ui_working_dir crab -create -cfg grid_theta_crab.cfg' % options.workdir,
    'cd %s; crab -submit -c crab' % options.workdir,
    'cd %s; crab -status -c crab' % options.workdir
]

import subprocess
for command in commands:
    print command
    subprocess.call( [command], shell=True )

