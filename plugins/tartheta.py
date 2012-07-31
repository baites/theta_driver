#
# Plugin to tar all theta files for further debugging. 
# Victor E. Bazterra UIC (2012)
#

from optparse import OptionParser

usage = 'usage: %prog tartheta [options]\n'
usage = usage + 'Tar all theta files for further debugging.'

parser = OptionParser(
    usage = usage
)

parser.add_option(
    '--workdir', type='string',
    help='Working directory of the driver."'
)

(options, args) = parser.parse_args()

command = 'tar cvfzh %s.tgz %s/analysis %s/analysis.py %s/utils.py %s/*.root' % (
    options.workdir, options.workdir, options.workdir, options.workdir, options.workdir
)

#command = 'tar cvfzh %s.tgz %s/analysis %s/analysis.py %s/utils.py' % (
#            options.workdir, options.workdir, options.workdir, options.workdir
#)

import subprocess
print command
subprocess.call(command, shell=True)

