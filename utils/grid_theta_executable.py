import subprocess
import glob
import copy
import re
import sys

print 'arguments on the command line are'
print sys.argv

index = int(sys.argv[1]) - 1

print 'Processing index = ' + str(index)


# Unpack the configs
s = 'tar -zxvf analysis.tgz'
print 'executing ' + s
subprocess.call( [s], shell=True )


# Get the analysis files
anaFilesRaw = glob.glob( 'analysis/*.cfg' )
anaFiles = sorted(anaFilesRaw)
print 'All analysis files are : '
print anaFiles
# Pick the one we're running on here. 
anaFile = anaFiles[index]
print 'Will be processing ' + anaFile

# Unpack the gridpack
print 'Unpacking the theta gridpack'
s = 'tar -zxvf gridpack.tgz'
print 'executing ' + s
subprocess.call( [s], shell=True )


# Now get the name of the logfile and output file
strippedName = copy.copy(anaFile)
strippedNameIndex1 = strippedName.find('/') + 1
strippedNameIndex2 = strippedName.find('.')
strippedName2 = strippedName[strippedNameIndex1:strippedNameIndex2]
print 'stripped name is ' + strippedName2

# Log file
logNameIndex1 = strippedName2.find('zp')
logNameIndex2 = strippedName2.find('--')
logName = 'debuglog' + strippedName2[logNameIndex1:logNameIndex2] + '.txt'
print 'log name is ' + logName

# Output file
outName = strippedName2 + '.db'
print 'output name is ' + outName


# Execute theta with the given config
s = 'bin/theta ' + anaFile + ' > /dev/null'
print 'executing ' + s
subprocess.call( [s], shell=True )

# tar up the results
print 'Tarring up the results to results.tgz'
s = 'tar -cz ' + logName + ' ' + outName + ' > results.tgz'
print 'executing ' + s
subprocess.call( [s], shell=True )

# removing local copies of the debug log
print 'Removing local copies the results to results.tgz'
s = 'rm -rf ' + logName + ' ' + outName
print 'executing ' + s
subprocess.call( [s], shell=True )

# List files
print 'Listing directory'
s = 'ls -trl .'
print 'executing ' + s
subprocess.call( [s], shell=True )
