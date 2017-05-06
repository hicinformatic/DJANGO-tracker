from script import writePidFile, deletePidFile, error, taskme
import csv, os, sys, urllib.request

scriptdir = os.path.dirname(os.path.realpath(__file__))
taskid = 1
port = sys.argv[1]
name = 'TRK_sort_recurring'
csvndatas = scriptdir + name + '.csv'

writePidFile(scriptdir, name)

taskme(port, 'start', taskid)

with urllib.request.urlopen("http://localhost:%s/tracker/ndatas.csv" % port) as response, open(csvndatas, 'wb') as out_file:
    data = response.read()
    out_file.write(data)

taskme(port, 'running', taskid)
taskme(port, 'complete', taskid)

deletePidFile(scriptdir, name)