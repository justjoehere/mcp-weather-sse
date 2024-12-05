# Issues with Starlette and MCP Servers
Starlette determines automatically determines whether the endpoint is an ASGI application or a 
function that accepts a Request object.


If you use functions, it assumes functions only take a Request object, so if you try to pass in scope, receive, and send
You'll get errors
```python
# This errors out
async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await weather_server.app.run(
            streams[0],
            streams[1],
            weather_server.app.create_initialization_options()
        )

async def handle_messages(request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

```
The error will look like 
```text
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 403, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\applications.py", line 113, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\middleware\errors.py", line 187, in __call__
    raise exc
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\middleware\errors.py", line 165, in __call__
    await self.app(scope, receive, _send)
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\routing.py", line 715, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\routing.py", line 735, in app
    await route.handle(scope, receive, send)
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\routing.py", line 288, in handle
    await self.app(scope, receive, send)
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\routing.py", line 76, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\xxxx\mcp-tutorial\.venv\Lib\site-packages\starlette\routing.py", line 74, in app
    await response(scope, receive, send)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'NoneType' object is not callable
```
So we need to define endpoints as classes so that we can get access to the scope, receive, and send objects

Example:

```python
def create_app():
    weather_server = WeatherServer()
    sse = SseServerTransport("/weather")

    class HandleSSE:
        def __init__(self, sse, weather_server):
            self.sse = sse
            self.weather_server = weather_server

        async def __call__(self, scope, receive, send):
            async with self.sse.connect_sse(scope, receive, send) as streams:
                await self.weather_server.app.run(
                    streams[0],
                    streams[1],
                    self.weather_server.app.create_initialization_options()
                )

    class HandleMessages:
        def __init__(self, sse):
            self.sse = sse

        async def __call__(self, scope, receive, send):
            await self.sse.handle_post_message(scope, receive, send)

    routes = [
        Route("/sse", endpoint=HandleSSE(sse, weather_server), methods=["GET"]),
        Route("/weather", endpoint=HandleMessages(sse), methods=["POST"])
    ]

    return Starlette(routes=routes)```