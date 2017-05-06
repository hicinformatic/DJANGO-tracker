from script import writePidFile, deletePidFile, error, taskme
import os, sys

scriptdir = os.path.dirname(os.path.realpath(__file__))
taskid = 1
port = sys.argv[1]
name = 'TRK_sort_recurring'

writePidFile(scriptdir, name)

taskme(port, 'start', taskid)
taskme(port, 'running', taskid)
taskme(port, 'complete', taskid)

deletePidFile(scriptdir, name)