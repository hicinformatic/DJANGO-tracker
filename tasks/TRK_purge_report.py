from script import writePidFile, deletePidFile, error, taskme
scriptdir = os.path.dirname(os.path.realpath(__file__))

writePidFile(scriptdir)

taskme('start')
taskme('running')
taskme('complete')

deletePidFile(scriptdir)