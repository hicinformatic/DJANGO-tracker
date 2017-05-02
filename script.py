def writePidFile(scriptdir, name):
    pid = str(os.getpid())
    f = open(scriptdir+'/'+name+'.pid', 'w')
    f.write(pid)
    f.close()

def deletePidFile(scriptdir):
    os.unlink(scriptdir+'/'+name+'.pid'.pid')

def error(task, message=''):
    errcurl = pycurl.Curl()
    if message is None or message == '': errcurl.setopt(errcurl.URL, "http://localhost/tracker/task/3/error/task.json")
    else: errcurl.setopt(errcurl.URL, "http://localhost/tracker/task/%s/error/task.json/%s"% (task, message)
    errcurl.perform()
    return errcurl.getinfo(pycurl.HTTP_CODE)

def taskme(command, task, message=''):
    taskcurl = pycurl.Curl()
    if message is None or message == '': taskcurl.setopt(taskcurl.URL, "http://localhost/tracker/task/%s/%s/task.json" % (task, command) )
    else: taskcurl.setopt(taskcurl.URL, "http://localhost/tracker/task/%s/%s/task.json/%s" % (task, command, message) )
    taskcurl.perform()
    code = taskcurl.getinfo(pycurl.HTTP_CODE)
    if code != 200: error()
    taskcurl.close()
    return code