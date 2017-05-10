from script import writePidFile, deletePidFile, error, taskme
import csv, os, sys, urllib.request, json

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
listid = []
visitors = {}
datas = {}

datas = { 'User-Agent': {}, 'AcceptLanguage': {}, 'datas': {}, 'events': {}, 'routes': {}, }
with open(csvndatas, newline='', encoding='utf-8') as csvfile:
    for row in csv.reader(csvfile, delimiter=','):
        try:
            visitors[row[5]][row[1]] = 1
        except Exception:
            visitors[row[5]] = { row[1]: 1, }
        listid.append(row[0])
        if row[3] == 'User-Agent':
            try:
                datas['User-Agent'][row[1]][row[8]] = row[4]
            except Exception:
                datas['User-Agent'][row[1]] = { row[8]: row[4] }
        elif row[3] == 'AcceptLanguage':
            try:
                datas['AcceptLanguage'][row[1]][row[8]] = row[4]
            except Exception:
                datas['AcceptLanguage'][row[1]] = { row[8]: row[4] }
        elif row[2] == 'True':
            try:
                datas['events'][row[1]][row[8]] =  { row[3]: row[4] }
            except Exception:
                datas['events'][row[1]] = { row[8]: { row[3]: row[4] }, }
        else:
            try:
                datas['datas'][row[1]][row[8]] =  { row[3]: row[4] }
            except Exception:
                datas['datas'][row[1]] = { row[8]: { row[3]: row[4] }, }
        try:
            datas['routes'][row[1]][row[8]] = { 'title': row[7], 'url': row[6] }
        except Exception:
            datas['routes'][row[1]] = { row[8]: { 'title': row[7], 'url': row[6] }, }


taskme(port, 'running', taskid, 'writejson')
with open(listidJSON, 'w') as outfile:
    json.dump(listid, outfile, indent=4)
with open(visitorsJSON, 'w') as outfile:
    json.dump(visitors, outfile, indent=4)
with open(datasJSON, 'w') as outfile:
    json.dump(datas, outfile, indent=4)

taskme(port, 'running', taskid, 'addjson')

taskme(port, 'complete', taskid)
deletePidFile(scriptdir, name)