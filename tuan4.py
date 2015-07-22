__author__ = 'techbk'

import asyncio
import sys

mport asyncio
from aiohttp import web

@asyncio.coroutine
def do_start(request):

    return web.Response(body=b"Start Process")

def check_result(request):


    return web.Response(body=b"")


app = web.Application()
app.router.add_route('GET', '/', do_start)
app.router.add_route('GET', '/', check_result)

loop = asyncio.get_event_loop()

handler = app.make_handler()
f = loop.create_server(handler,'127.0.0.1', 8080)
print("Server started at http://127.0.0.1:8080")

srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(handler.finish_connections(1.0))
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.finish())
loop.close()
