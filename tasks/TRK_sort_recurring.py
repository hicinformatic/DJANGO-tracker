from script import writePidFile, deletePidFile, error, taskme
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))
taskid = 1
name = 'TRK_sort_recurring'

writePidFile(scriptdir, name)

taskme('start', taskid)
taskme('running', taskid)
taskme('complete', taskid)

deletePidFile(scriptdir, name)