from script import writePidFile, deletePidFile, error, taskme
import csv, os, sys, urllib.request, json, hashlib

scriptdir = os.path.dirname(os.path.realpath(__file__))
taskid = 1
port = sys.argv[1]
name = 'TRK_sort_recurring'
csvndatas = scriptdir + '/' + name + '.csv'
listidJSON =  scriptdir + '/' + name + '_listid.json'
visitorsJSON = scriptdir + '/' + name + '_visitors.json'
datasJSON =  scriptdir + '/' + name + '_datas.json'

writePidFile(scriptdir, name)
taskme(port, 'start', taskid)

taskme(port, 'running', taskid, 'getcsv')
with urllib.request.urlopen("http://localhost:%s/tracker/ndatas.csv" % port) as response, open(csvndatas, 'wb') as out_file:
    data = response.read()
    out_file.write(data)

taskme(port, 'running', taskid, 'readcsv')
#listid = []
#visitors = {}

datas = { 'useragents': {}, 'acceptlanguages': {}, 'routes': {}, 'datas': {}, 'events': {},  'visitors': [], 'id': [] }
sorts = { 'User-Agent': 'useragents', 'AcceptLanguage': 'acceptlanguages', 'route': 'routes' }
with open(csvndatas, newline='', encoding='utf-8') as csvfile:
    for row in csv.reader(csvfile, delimiter=','):
        duplicate = hashlib.md5(row[1] + row[3] + row[4]).digest()     
        if any(row[3] in key for key in sorts):
            datas[sorts[row[3]]][duplicate] = { 'user': row[1], 'date': row[8], 'data': row[4], 'url': row[6], 'title': row[7] }
        else:
            key = 'events' if row[2] == 'True' else 'datas'
            datas[key][row[1]][duplicate] = { 'user': row[1], 'date': row[8], 'data': row[4], 'url': row[6], 'title': row[7] }
        if row[1] not in datas['visitors']: datas['visitors'].append(row[1])
        datas['id'].append(row[0])


taskme(port, 'running', taskid, 'writejson')
#with open(listidJSON, 'w') as outfile:
#    json.dump(listid, outfile, indent=4)
#with open(visitorsJSON, 'w') as outfile:
#    json.dump(visitors, outfile, indent=4)
with open(datasJSON, 'w') as outfile:
    json.dump(datas, outfile, indent=4)

#taskme(port, 'running', taskid, 'subtaskVistor')
#sub = urllib.request.urlopen("http://localhost:%s/tracker/1/0/subtask.json" % port)
#if sub.getcode() != 200: error(port, task, message='subtaskVistor')
#
#taskme(port, 'running', taskid, 'subtaskAllinfos')
#sub =urllib.request.urlopen("http://localhost:%s/tracker/1/1/subtask.json" % port)
#if sub.getcode() != 200: error(port, task, message='subtaskAllinfos')
#
#taskme(port, 'running', taskid, 'subtaskDelTracedSort')
#sub =urllib.request.urlopen("http://localhost:%s/tracker/1/2/subtask.json" % port)
#if sub.getcode() != 200: error(port, task, message='subtaskDelTracedSort')
#
#os.unlink(csvndatas)
#os.unlink(visitorsJSON)
#os.unlink(datasJSON)
#os.unlink(listidJSON)


taskme(port, 'complete', taskid)
deletePidFile(scriptdir, name)