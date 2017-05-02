import urllib.request, os

def writePidFile(scriptdir, name):
    pid = str(os.getpid())
    f = open(scriptdir+'/'+name+'.pid', 'w')
    f.write(pid)
    f.close()

def deletePidFile(scriptdir, name):
    os.unlink(scriptdir+'/'+name+'.pid')

def error(task, message=''):
    if message is None or message == '': c = urllib.request.urlopen("http://localhost:26080/tracker/task/3/error/task.json")
    else: c = urllib.request.urlopen("http://localhost:26080/tracker/task/%s/error/task.json/%s"% (task, message) )
    return c.getcode()

def taskme(command, task, message=''):
    if message is None or message == '': c = urllib.request.urlopen("http://localhost:26080/tracker/task/%s/%s/task.json" % (task, command) )
    else: c = urllib.request.urlopen("http://localhost:26080/tracker/task/%s/%s/task.json/%s" % (task, command, message) )
    code = c.getcode()
    if code != 200: error()
    return code