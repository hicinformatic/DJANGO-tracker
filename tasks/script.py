import urllib.request, os

def writePidFile(scriptdir, name):
    pid = str(os.getpid())
    f = open(scriptdir+'/'+name+'.pid', 'w')
    f.write(pid)
    f.close()

def deletePidFile(scriptdir, name):
    os.unlink(scriptdir+'/'+name+'.pid')

def error(port, task, message=''):
    if message is None or message == '': c = urllib.request.urlopen("http://localhost:%s/tracker/task/3/error/task.json" % port)
    else: c = urllib.request.urlopen("http://localhost:%s/tracker/task/%s/error/task.json/%s" % (port, task, message) )
    return c.getcode()

def taskme(port, command, task, message=''):
    if message is None or message == '': c = urllib.request.urlopen("http://localhost:%s/tracker/task/%s/%s/task.json" % (port, task, command) )
    else: c = urllib.request.urlopen("http://localhost:%s/tracker/task/%s/%s/task.json/%s" % (port, task, command, message) )
    code = c.getcode()
    if code != 200: error()
    return code