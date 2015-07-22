__author__ = 'techbk'

import asyncio
from aiohttp import web
import datetime
import functools
import sys


class Url_handler:
    def __init__( self,loop ):
        self._loop = loop
        self._task = {}
        self._taskid = 0

    @asyncio.coroutine
    def do_start( self,request ):
        task_run_process = asyncio.async( run_process( 10 ) )
        task_run_process.add_done_callback( got_result )
        self._taskid = self._taskid + 1
        id = str( self._taskid )
        text = "Do Start App: http://localhost:8080/checkresult/" + id
        self._task[id] = task_run_process

        return web.Response( body = text.encode( 'utf-8' ) )

    @asyncio.coroutine
    def check_result( self,request ):
        id = request.match_info.get( 'id' )
        if id:
            task_run_process = self._task.get(id,False)
            #assert isinstance( task_run_process,asyncio.Task )
            if task_run_process:
                if task_run_process.done():
                    print( task_run_process.done( ) )

                    result = yield from task_run_process
                    print( result )
                    if result[1]:
                        text = "App " + id + " error:" + result[1].decode('ascii')
                        return web.Response( body = text.encode( 'utf-8' ) )

                    # return web.Response(body=result)
                    text = "App " + id + " done!"
                    return web.Response( body = text.encode( 'utf-8' ) )
                else:
                    text = "App Not Done"
                    return web.Response( body = text.encode( 'utf-8' ) )

            else:
                text = "App ko ton tai"
                return web.Response( body = text.encode( 'utf-8' ) )
        else:
            text = "Link cua ban ko ton tai"
            return web.Response( body = text.encode( 'utf-8' ) )



def got_result( future ):
    print( future.result( ) )


@asyncio.coroutine
def run_process( time ):

    assert isinstance( time,int )
    code = u'import time; print("Sleep {time:d}"); time.sleep({time:d})'.format( **{"time": time} )


    print( 'Chuong trinh OK' )
    print( datetime.datetime.now() )

    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_exec( sys.executable,'-c',code,
                                             stdout = asyncio.subprocess.PIPE,stderr = asyncio.subprocess.PIPE )
    # Wait for create
    proc = yield from create  # proc is Process Instance

    out,err = yield from proc.communicate()

    return out,err


@asyncio.coroutine
def index( request ):
    return web.Response( body = b"Welcome" )



@asyncio.coroutine
def init( loop ):
    url_handler = Url_handler( loop )

    app = web.Application( loop = loop )

    app.router.add_route( 'GET','/',index )
    app.router.add_route( 'GET','/dostart',url_handler.do_start )
    app.router.add_route( 'GET','/checkresult/{id}',url_handler.check_result )


    handler = app.make_handler( )
    srv = yield from loop.create_server( handler,
                                         '127.0.0.1',8080 )
    print( "Server started at http://127.0.0.1:8080" )
    return srv,handler


loop = asyncio.get_event_loop( )
srv,handler = loop.run_until_complete( init( loop ) )

try:
    loop.run_forever( )
except KeyboardInterrupt:
    pass
