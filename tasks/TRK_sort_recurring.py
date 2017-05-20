from script import writePidFile, deletePidFile, error, taskme
import csv, os, sys, urllib.request, json, hashlib

scriptdir = os.path.dirname(os.path.realpath(__file__))
taskid = 1
port = sys.argv[1]
name = 'TRK_sort_recurring'
csvndatas = scriptdir + '/' + name + '.csv'
propsJSON =  scriptdir + '/' + name + '.json'

writePidFile(scriptdir, name)
taskme(port, 'start', taskid)

taskme(port, 'running', taskid, 'getcsv')
with urllib.request.urlopen("http://localhost:%s/tracker/ndatas.csv" % port) as response, open(csvndatas, 'wb') as out_file:
    data = response.read()
    out_file.write(data)

taskme(port, 'running', taskid, 'readcsv')
datas = { 'useragents': {}, 'acceptlanguages': {}, 'routes': {}, 'datas': {}, 'events': {}, }
props = { 'useragents': [], 'acceptlanguages': [], 'routes': [], 'datas': [], 'events': [],  'visitors': {}, 'id': [], 'domains': [] }
sorts = { 'User-Agent': 'useragents', 'AcceptLanguage': 'acceptlanguages', 'route': 'routes' }
with open(csvndatas, newline='', encoding='utf-8') as csvfile:
    for row in csv.reader(csvfile, delimiter=','):
        duplicate = row[1] + row[3] + row[4]
        duplicate = duplicate.encode('utf-8')
        duplicate = hashlib.md5(duplicate).hexdigest()
        if any(row[3] in key for key in sorts):
            datas[sorts[row[3]]][duplicate] = { 'user':row[1], 'date':row[8], 'data':row[4], 'url':row[6], 'title':row[7] }
        else:
            datatype = 'events' if row[2] == 'True' else 'datas'
            datas[datatype][duplicate] = { 'user':row[1], 'date':row[8], 'type':row[3], 'data':row[4], 'url':row[6], 'title':row[7] }
        if row[1] not in props['visitors']: props['visitors'][row[1]] = row[5]
        if row[5] not in props['domains']: props['domains'].append(row[5])
        props['id'].append(row[0])

for key,value in datas.items():
    for k,v in value.items():
        if key in ['datas', 'events']:
            props[key].append({ 'visitor':v['user'], 'key':v['type'], 'value':v['data'], 'title':v['title'], 'url':v['url'], 'create':v['date'] })
        if key == 'routes':
            props[key].append({ 'visitor':v['user'], 'title':v['title'], 'url':v['url'], 'load':v['data'], 'create':v['date']  })
        if key == 'useragents':
            props[key].append({ 'visitor':v['user'], 'useragent':v['data'], 'create':v['date'] })
        if key == 'acceptlanguages':
            props[key].append({ 'visitor':v['user'], 'acceptlanguage':v['data'], 'create':v['date'] })
taskme(port, 'running', taskid, 'writejson')

with open(propsJSON, 'w') as outfile:
    json.dump(props, outfile, indent=4)

taskme(port, 'running', taskid, 'subtaskVisitor')
#sub = urllib.request.urlopen("http://localhost:%s/tracker/1/0/subtask.json" % port)
#if sub.getcode() != 200: error(port, task, message='subtaskVistor')
#
taskme(port, 'running', taskid, 'subtaskAllinfos')
#sub =urllib.request.urlopen("http://localhost:%s/tracker/1/1/subtask.json" % port)
#if sub.getcode() != 200: error(port, task, message='subtaskAllinfos')
#
taskme(port, 'running', taskid, 'subtaskDelTracedSort')
#sub =urllib.request.urlopen("http://localhost:%s/tracker/1/2/subtask.json" % port)
#if sub.getcode() != 200: error(port, task, message='subtaskDelTracedSort')
#
#os.unlink(csvndatas)
#os.unlink(propsJSON)


taskme(port, 'complete', taskid)
deletePidFile(scriptdir, name)