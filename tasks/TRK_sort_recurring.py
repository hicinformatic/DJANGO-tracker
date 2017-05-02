from script import writePidFile, deletePidFile, error, taskme
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))
taskid = 1

writePidFile(scriptdir)

taskme(taskid, 'start')
taskme(taskid, 'running')
taskme(taskid, 'complete')

deletePidFile(scriptdir)