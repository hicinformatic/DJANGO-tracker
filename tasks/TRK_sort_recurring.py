from script import writePidFile, deletePidFile, error, taskme
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))
taskid = 1
name = 'TRK_sort_recurring'

writePidFile(scriptdir, name)

taskme(taskid, 'start')
taskme(taskid, 'running')
taskme(taskid, 'complete')

deletePidFile(scriptdir, name)