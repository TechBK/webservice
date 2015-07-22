__author__ = 'techbk'

import asyncio.subprocess
import sys
import datetime

def call_ur_process():
    result = loop.run_until_complete(get_date(5))
    print("Process: %s" %result[0].decode('ascii'))
    if result[1]:
        print("Process: %s" %result[1].decode('ascii'))

@asyncio.coroutine
def get_date(time):
    #stringcode(5)
    #print(code(5))
    assert isinstance( time,int)
    code = u'import time; time.sleep({time:d})'.format( **{"time": time} )
    #code = "import time; print("Sleep %d"); time.sleep(%(time)d)"%{"time":5}
    print(datetime.datetime.now())
    print('Sleep %d'%time)

    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_exec(sys.executable, '-c', code,
                                            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    # Wait for create
    proc = yield from create    #proc is Process Instance

    out , err = yield from proc.communicate()

    return out , err

#if sys.platform == "win32":
    #loop = asyncio.ProactorEventLoop()
    #asyncio.set_event_loop(loop)
#else:
loop = asyncio.get_event_loop()

call_ur_process()

loop.close()