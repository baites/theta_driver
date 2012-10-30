#
# Getouput plugin to collect all the outputs from crab and SE
# Victor E. Bazterra UIC (2012)
#

from optparse import OptionParser

usage = 'usage: %prog getouput [options]\n'
usage = usage + 'Collect all the outputs from crab sandbox or SE.'

parser = OptionParser(
    usage = usage 
)

parser.add_option(
    '--workdir', type='string',
    help='Working directory of the driver."'
)
parser.add_option(
    '--remoteurl', type='string',
    help='Remote url of the directory to get all the produced theta files."'
)

(options, args) = parser.parse_args()

cmds = [
    'cd %s; crab -getoutput -c crab' % options.workdir,
    'mkdir %s/analysis/cache' % options.workdir
]

import commands, os

if options.remoteurl:
    output = commands.getstatusoutput('lcg-ls %s' % options.remoteurl)
    if output[0] == 0:
        for file in output[1].split('\n'):
            file = os.path.basename(file)
            cmds.append('lcg-cp -D srmv2 %s/%s file:///%s/analysis/cache/%s' % (
                options.remoteurl, file, os.path.abspath(options.workdir), file
            ))
            cmds.append('cd %s/analysis/cache; tar xfz %s; rm %s' % (options.workdir, file, file))
else:
    output = commands.getstatusoutput('ls %s/crab/res/*.tgz' % options.workdir)
    for file in output[1].split('\n'):
        cmds.append('mv %s %s/analysis/cache; cd %s/analysis/cache; tar xfz %s; rm %s' % (file, options.workdir, options.workdir, os.path.basename(file), os.path.basename(file)))

import subprocess
for cmd in cmds:
    print cmd
    subprocess.call( [cmd], shell=True )

